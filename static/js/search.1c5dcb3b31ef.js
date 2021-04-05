const searchField = document.querySelector('#searchField');
const tableOutput = document.getElementById("tableOutput");
const appTable = document.getElementById("appTable");
const tableBodyOutput = document.getElementById("tableBodyOutput");

tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) =>{
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    tableBodyOutput.innerHTML = ""
    fetch("/search-customer", {
      body: JSON.stringify({ searchText: searchValue}),
      method: "POST",
    })
      .then(res=>res.json())
      .then(data=> {
        appTable.style.display = 'none';
        tableOutput.style.display = 'block';
        if (data.length === 0) {
          tableOutput.style.display = 'none';
        } else {
          data.forEach((item) => {
            tableBodyOutput.innerHTML += `
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
            `;
          });
        }
      });   
  }
});