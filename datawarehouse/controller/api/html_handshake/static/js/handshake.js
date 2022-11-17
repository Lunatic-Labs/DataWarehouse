//keeps track of the number of metrics belonging to each source (# sources = array length)
var num_metrics = [1];

//takes the ID of a div in the format "0.0" (a string) and slices/parses it to find the 
//source and metric number (returns [0, 0] both ints)
function findIndices(ID_name) {
    var index = ID_name.indexOf(".");
    var src = parseInt(ID_name.slice(0, index));
    var metric = parseInt(ID_name.slice(index + 1));
    return [src, metric];
}

// takes the outer div (the one that will hold all the info for a source) and creates an inner
// div that will either hold (1) overview info about the source, or (2) info about the first metric 
// defined for a source 
// inner_div_template will pertain to either (1) overview info, or (2) source #1 info
// ovr_or_metric: true -> create overview div; false -> create source #1 div
function createInnerDivs(outer_div, inner_div_template, ovr_or_metric) {
    var new_inner_div = document.createElement('div');
    if (ovr_or_metric)
        new_inner_div.id = (num_metrics.length - 1) + ".overview";
    else
        new_inner_div.id = (num_metrics.length - 1) + ".0";
    new_inner_div.innerHTML = inner_div_template.innerHTML;
    outer_div.appendChild(new_inner_div);
}

function addSource() {
    //each new source must have at least 2 elements--overview info and 
    //info for at least one metric. Copy these two items from the most recent
    //source added
    var overview = document.getElementById((num_metrics.length - 1) + ".overview");
    var first_metric = document.getElementById((num_metrics.length - 1) + ".0");

    //extend array to account for new source
    num_metrics.push(1);

    //create new source (outer) div that will hold the divs for the overview/metric info
    var new_source = document.createElement('div');
    new_source.id = 'source' + (num_metrics.length - 1);
    document.getElementsByTagName('form')[0].appendChild(new_source);

    //create new inner divs that will contain overview info and metric #1 info about the
    // new source
    createInnerDivs(new_source, overview, true);
    createInnerDivs(new_source, first_metric, false);
}

function addMetric(element) {
    //get name of div ID where the button was clicked
    var ID_name = element.parentNode.id;

    //get index of source for new div, so we can add it to the right section on the page
    var indices = findIndices(ID_name);

    //get contents of a previous metric info div to copy into the new one (acts as a template)
    var last_metric = document.getElementById("0.0");

    //create new metric info div; give it the correct ID name and copy the fields from the template
    var new_metric = document.createElement("div");
    new_metric.id = indices[0] + "." + num_metrics[indices[0]];
    new_metric.innerHTML = last_metric.innerHTML;

    //append the div to the correct source
    var current_src = document.getElementById("source" + indices[0]);
    current_src.appendChild(new_metric)

    //the current source now has one more metric
    num_metrics[indices[0]] += 1;
}

function removeMetric(element) {
    //get name of div ID where the button was clicked
    var ID_name = element.parentNode.id;

    //get name of outer div ("source0"--for later)
    var div_name = document.getElementById(element.parentNode.parentNode.id);

    //get index of source for new div, so we can add it to the right section on the page
    var indices = findIndices(ID_name);

    //if only one metric defined, don't allow user to delete metric...
    if (num_metrics[indices[0]] == 1) {
        window.alert("At least one metric must be defined for each source");
        return;
    }

    //...if more than one metric defined, let user delete the source...
    var div_id = document.getElementById(ID_name);
    div_id.remove();
    num_metrics[indices[0]] -= 1;

    //...then update the inner div names so there are no gaps (ex. _.0 is 1st, _.1 is 2nd, etc.)
    //get list of inner div names; 1st element is "_.overview"
    var metric_names = div_name.getElementsByTagName('div');
    var i, j;
    for (i = 1, j = 0; i < metric_names.length; i++, j++)
        metric_names[i].id = `${indices[0]}.${j}`;
}

function removeSource(element) {
    var outer_div = element.parentNode.parentNode; //"source0" div

    //if only one source has been defined, do not allow the user to delete it...
    if (num_metrics.length == 1) {
        window.alert("At least one source must be defined on the form")
        return;
    }

    //...otherwise, delete it
    outer_div.remove();

    //get source number for later
    var src_index = outer_div.id.indexOf("e");
    var src_num = parseInt(outer_div.id.slice(src_index + 1));

    //iterate over both inner and outer div names, and change them to reflect 
    //the correct enumeration
    var metric_names = document.getElementsByTagName("div");
    for (var i = 0, j = -1; i < metric_names.length; i++) {
        // "source0" 
        if (metric_names[i].id.indexOf("source") != -1) {
            j += 1;
            metric_names[i].id = "source" + j;
        }
        // "0.overview"
        else if (metric_names[i].id.indexOf("overview") != -1) {
            metric_names[i].id = j + ".overview";
        }
        // "0.0", "0.1", etc.
        else {
            var suffix_index = metric_names[i].id.indexOf(".");
            var suffix = metric_names[i].id.slice(suffix_index);
            metric_names[i].id = j + suffix;
        }
    }

    //pop correct element from array so that another source can be added while 
    //keeping the correct enumeration intact
    num_metrics.splice(src_num, 1);
}

//get list of html elements to change to "Source #1", "Source #2", etc.
var src_titles = document.getElementsByTagName("h2");

//get list of html elements to change to the following format:
//"Metric #1 for Source #1"
var metric_titles = document.getElementsByTagName("h3");

document.addEventListener("click", function () {
    //change source headers to reflect correct enumeration
    for (var i = 0; i < src_titles.length; i++) {
        src_titles[i].innerHTML = `Source #${i + 1}`;
    }

    //change metric headers to reflect correct enumeration
    for (var i = 0; i < metric_titles.length; i++) {
        //get ID of div ("0.0", "1.2", etc.)
        var ID_name = metric_titles[i].parentNode.id;

        //get source/metric numbers of the div ID
        var indices = findIndices(ID_name);

        //change the heading
        metric_titles[i].innerHTML = `Metric #${indices[1] + 1} for Source #${indices[0] + 1}`;
    }
});