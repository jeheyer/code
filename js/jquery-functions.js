  // Generic function to make AJAX call
  async function GetAJAXData(url, args = {}) {
    let results = new Array();
    try {
      results = await $.ajax({
        url: url,
        data: args,
        type: 'GET',
        dataType: 'json'
      });
      return results;
    } catch (error) {
      console.error(error);
    }
  }

  // Parse get parameters
  var get_params = {}
  location.search.substr(1).split("&").forEach(function(item) {get_params[item.split("=")[0]] = item.split("=")[1]})


function FillTable(table_id, data) {

    // Set alternating table row background colors
    $(document).ready(function(){
        $("table tr:even").css("background-color", "#fefefe");
        $("table tr:odd").css("background-color", "#efefef");
    });

    // Fill Table Header
    $(`#${table_id} thead`).empty();
    let table_head_html = "<tr>";
    for (let key in data[0]) {
        table_head_html += "<th>" + key + "</th>";
    }
    table_head_html += "</tr>";
    $(`#${table_id} thead`).append(table_head_html);
        
    // Fill Table Body
    $(`#${table_id} tbody`).empty();
    $.each(data, function(index, obj) {
        let row_html = "<tr>";
        for (let key in obj) {
            if (Array.isArray(obj)) {
                row_html += "<td>" + "array" + "</td>"
            } else {
                let value = obj[key];
                if (key != "calendarYear") 
                    value = "$ " + parseFloat(value.toFixed(2)).toLocaleString();
                row_html += "<td>" + value + "</td>";
            }
        }
        row_html += "</tr>";
        $(`#${table_id}`).append(row_html);
    });
}
