var source = 0;
var metric = 0;
var num_metrics = [];

function addSource() {
    var overview = document.getElementById("source" + num_metrics.length + "_overview");

    var first_metric = document.getElementById("source" + num_metrics.length + "_metric0");

    num_metrics.push(1);

    source += 1;
    metric = 0;
    var new_source = document.createElement('div');
    new_source.id = 'source' + num_metrics.length;
    document.getElementsByTagName('form')[0].appendChild(new_source);

    var new_source_overview = document.createElement('div');
    new_source_overview.id = "source" + num_metrics.length + "_overview";

    var new_first_metric = document.createElement('div');
    new_first_metric.id = "source" + num_metrics.length + "_metric0";
    new_first_metric.className = num_metrics.length;

    new_source_overview.innerHTML = overview.innerHTML;
    new_first_metric.innerHTML = first_metric.innerHTML;

    new_source.appendChild(new_source_overview);
    new_source.appendChild(new_first_metric);
}

function addMetric() {
    var last_metric = document.getElementById("source" + source + "_metric" + metric);
    var current_src = document.getElementById("source" + source);

    metric += 1;
    var new_metric = document.createElement("div");
    new_metric.id = "source" + source + "_metric" + metric;

    new_metric.innerHTML = last_metric.innerHTML;

    current_src.appendChild(new_metric);
}
