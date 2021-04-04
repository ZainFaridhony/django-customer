const searchField=document.querySelector('#searchField');const tableOutput=document.getElementById("tableOutput");const appTable=document.getElementById("appTable");const tableBodyOutput=document.getElementById("tableBodyOutput");tableOutput.style.display="none";searchField.addEventListener("keyup",(e)=>{const searchValue=e.target.value;if(searchValue.trim().length>0){tableBodyOutput.innerHTML=""
fetch("/search-customer",{body:JSON.stringify({searchText:searchValue}),method:"POST",}).then(res=>res.json()).then(data=>{appTable.style.display='none';tableOutput.style.display='block';if(data.length===0){tableOutput.style.display='none';}else{data.forEach((item)=>{tableBodyOutput.innerHTML+=`
              <tr>
                <td><a href="/edit-customer/${item.id}">${item.first_name}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.middle_name}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.last_name}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.age}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.gender}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.status}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.phone_number}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.address}</a></td>
                <td><a href="/edit-customer/${item.id}">${item.company_name}</a></td>                
                <td><a href="/edit-customer/${item.id}">${item.income}</a></td>
              </tr>
            `;});}});}});;const renderBarChart=(customerdata)=>{google.charts.load('current',{'packages':['bar']});google.charts.setOnLoadCallback(drawChart);function drawChart(){var data=google.visualization.arrayToDataTable(customerdata[0]);var options={legend:{position:"none"},chart:{},hAxis:{title:'Age',},vAxis:{title:'Income',}};var chart=new google.charts.Bar(document.getElementById('columnchart_material'));chart.draw(data,google.charts.Bar.convertOptions(options));}}
const renderGenderBarChart=(genderdata)=>{google.charts.load('current',{'packages':['bar']});google.charts.setOnLoadCallback(drawChart);function drawChart(){var data=google.visualization.arrayToDataTable(genderdata[0]);var options={chart:{},legend:{position:'none'},bars:'horizontal'};var chart=new google.charts.Bar(document.getElementById('barchart_material'));chart.draw(data,google.charts.Bar.convertOptions(options));}}
const getChartData=()=>{fetch('customer_summary').then(res=>res.json()).then(data=>{renderBarChart([data.age_income_data]);renderGenderBarChart([data.gender_data]);})}
document.onload=getChartData();;