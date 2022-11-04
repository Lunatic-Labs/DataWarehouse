//var i = 0;
//var original = document.getElementById('duplicater' + i);
//var clone = original.cloneNode(true); // "deep" clone
//function duplicate(id) {
//    clone.id = id + ++i;
//    original.parentNode.appendChild(clone);
//}

var source = 0;
var metric = 0;

function duplicate(id) {
    var original = document.getElementById(id + i);
    var clone = original.cloneNode(true); // "deep" clone

    //clone.querySelector('.src_name').value = '';
    //clone.querySelector('.metric_name').value = '';
    //clone.querySelector('.units').value = '';

    clone.id = id + ++i; // there can only be one element with an ID
    clone.onclick = duplicate; // event handlers are not cloned
    original.parentNode.appendChild(clone);
}

function addSource() {
    var overview = document.getElementById("source" + source + "_overview");
    var overview_clone = overview.cloneNode(true);

    var first_metric = document.getElementById("source" + source + "_metric0");
    var first_metric_clone = first_metric.cloneNode(true);

    source += 1;
    var new_source = document.createElement('div');
    new_source.id = 'source' + source;
    document.getElementsByTagName('form')[0].appendChild(new_source);

    var new_source_overview = document.createElement('div');
    new_source_overview.className = "source" + source + "_overview";

    var new_first_metric = document.createElement('div');
    new_first_metric.className = "source" + source + "_metric0";

    new_source_overview.innerHTML = overview.innerHTML;
    new_first_metric.innerHTML = first_metric.innerHTML;

    new_source.appendChild(new_source_overview);
    new_source.appendChild(new_first_metric);
}

function flap() {
    // Your existing code unmodified...
    var iDiv = document.createElement('div');
    iDiv.id = 'block';
    iDiv.className = 'block';
    document.getElementsByTagName('form')[0].appendChild(iDiv);

    // Now create and append to iDiv
    var innerDiv = document.createElement('div');
    innerDiv.className = 'block-2';

    var innerDiv2 = document.createElement('div');
    innerDiv2.className = 'block-3';

    // The variable iDiv is still good... Just append to it.
    iDiv.appendChild(innerDiv);
    iDiv.appendChild(innerDiv2);
}