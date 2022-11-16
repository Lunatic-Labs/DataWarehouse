//keeps track of the number of metrics belonging to each source (# sources = array length)
var num_metrics = [1];

function addSource() {
    //each new source must have at least 2 elements--overview info and 
    //info for at least one metric. Copy these two items from the most recent
    //source added
    var overview = document.getElementById((num_metrics.length - 1) + ".overview");
    var first_metric = document.getElementById((num_metrics.length - 1) + ".0");

    //extend array to account for new source
    num_metrics.push(1);

    //create new source div that will hold the divs for the overview/metric info
    var new_source = document.createElement('div');
    new_source.id = 'source' + (num_metrics.length - 1);
    document.getElementsByTagName('form')[0].appendChild(new_source);

    //create div for overview info for new source, and put it inside the new source div
    var new_source_overview = document.createElement('div');
    new_source_overview.id = (num_metrics.length - 1) + ".overview";
    new_source_overview.innerHTML = overview.innerHTML;
    new_source.appendChild(new_source_overview);

    //the same thing as above, but for the div containing info about the first new metric
    var new_first_metric = document.createElement('div');
    new_first_metric.id = (num_metrics.length - 1) + ".0";
    new_first_metric.innerHTML = first_metric.innerHTML;
    new_source.appendChild(new_first_metric);
}

function addMetric(element) {
    //window.alert(element.id);
    //get name of div ID where the button was clicked
    var ID_name = element.parentNode.id;

    //get index of source for new div, so we can add it to the right section on the page
    var index = ID_name.indexOf(".");
    var src = parseInt(ID_name.slice(0, index));

    //get contents of a previous metric info div to copy into the new one (acts as a template)
    var last_metric = document.getElementById("0.0");

    //create new metric info div; give it the correct ID name and copy the fields from the template
    var new_metric = document.createElement("div");
    new_metric.id = src + "." + num_metrics[src];
    new_metric.innerHTML = last_metric.innerHTML;

    //append the div to the correct source
    var current_src = document.getElementById("source" + src);
    current_src.appendChild(new_metric)

    //the current source now has one more metric
    num_metrics[src] += 1;
}

function removeMetric(element) {
    //get name of div ID where the button was clicked
    var ID_name = element.parentNode.id;

    //get name of outer div ("source0"--for later)
    var div_name = document.getElementById(element.parentNode.parentNode.id);

    //get index of source for new div, so we can add it to the right section on the page
    var index = ID_name.indexOf(".");
    var src = parseInt(ID_name.slice(0, index));

    //if only one metric defined, don't allow user to delete metric...
    if (num_metrics[src] == 1) {
        window.alert("At least one metric must be defined for each source");
        return;
    }

    //...if more than one metric defined, let user delete the source...
    var div_id = document.getElementById(ID_name);
    div_id.remove();
    num_metrics[src] -= 1;

    //...then update the inner div names so there are no gaps (ex. _.0 is 1st, _.1 is 2nd, etc.)
    //get list of inner div names; 1st element is "_.overview"
    var metric_names = div_name.getElementsByTagName('div');
    var i, j;
    for (i = 1, j = 0; i < metric_names.length; i++, j++)
        metric_names[i].id = `${src}.${j}`;
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

        //find source and metric number of ID_name by slicing the string
        var index = ID_name.indexOf(".");
        var src = parseInt(ID_name.slice(0, index));
        var metric = parseInt(ID_name.slice(index + 1));

        //change the heading
        metric_titles[i].innerHTML = `Metric #${metric + 1} for Source #${src + 1}`;
    }
});