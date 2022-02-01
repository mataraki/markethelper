document.addEventListener('DOMContentLoaded', function() {

  fetch('https://freecurrencyapi.net/api/v2/latest?apikey=b4e6b7c0-73a0-11ec-9e82-f1084934855b')
  .then(response => response.json())
  .then(data => {
      usdtorub = data.data.RUB;
  });

  fetch('https://freecurrencyapi.net/api/v2/latest?apikey=b4e6b7c0-73a0-11ec-9e82-f1084934855b&base_currency=EUR')
  .then(response => response.json())
  .then(data => {
      eurtorub = data.data.RUB;
  });

  // Buttons in portfolio
  document.querySelector('#deposit-button').addEventListener('click', () => show_form('deposit'));
  document.querySelector('#buy-button').addEventListener('click', () => show_form('buy'));
  document.querySelector('#sell-button').addEventListener('click', () => show_form('sell'));

  // Refresh button
  document.querySelector('#refresh').addEventListener('click', () => quote());

  // Forms in portfolio
  document.querySelector('#deposit-form').onsubmit = function(event) {
    // Prevent form from realoding the page
    event.preventDefault();
    // Deposit the funds
    fetch('/deposit', {
      method: 'POST',
      body: JSON.stringify(document.querySelector('#deposit-amount').value)
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    invested = parseFloat(invested) + parseFloat(document.querySelector('#deposit-amount').value);
    document.querySelector('#portfolio-invested').innerHTML = `<h5>Invested: ${invested.toFixed(2)}</h5>`;
    clear_forms();

    setTimeout(function(){refresh_shares()}, 100);
  };

  document.querySelector('#buy-form').onsubmit = function(event) {
    // Prevent form from realoding the page
    event.preventDefault();
    // Buy the shares
    fetch('/buy', {
      method: 'POST',
      body: JSON.stringify({
        type: document.querySelector('#buy-type').value,
        ticker: document.querySelector('#buy-ticker').value,
        name: document.querySelector('#buy-name').value,
        quantity: document.querySelector('#buy-quantity').value,
        price: document.querySelector('#buy-price').value,
        currency: document.querySelector('#buy-currency').value,
        rating: document.querySelector('#buy-rating').value
    })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    clear_forms();

    setTimeout(function(){refresh_shares()}, 100);
  };

  document.querySelector('#sell-form').onsubmit = function(event) {
    // Prevent form from realoding the page
    event.preventDefault();
    // Sell the shares
    fetch('/sell', {
      method: 'POST',
      body: JSON.stringify({
        ticker: document.querySelector('#sell-ticker').value,
        quantity: document.querySelector('#sell-quantity').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    clear_forms();
    
    setTimeout(function(){refresh_shares()}, 100);
  };

  let stockstable = new DataTable('#stocks-table', {
    "searching": false,
    "paging": false,
    "info": false,
    "order": [],
    "columnDefs": [
      { orderable: false, "width": "30%", "targets": 0 },
      { orderable: false, "width": "10%", "targets": 1 },
      { orderable: false, "width": "20%", "targets": 2 },
      { orderable: false, "width": "20%", "targets": 3 },
      { orderable: false, "width": "10%", "targets": 4 },
      { orderable: false, "width": "10%", "targets": 5 }
    ]
  });

  let etfstable = new DataTable('#etfs-table', {
    "searching": false,
    "paging": false,
    "info": false,
    "order": [],
    "columnDefs": [
      { orderable: false, "width": "30%", "targets": 0 },
      { orderable: false, "width": "10%", "targets": 1 },
      { orderable: false, "width": "20%", "targets": 2 },
      { orderable: false, "width": "20%", "targets": 3 },
      { orderable: false, "width": "10%", "targets": 4 },
      { orderable: false, "width": "10%", "targets": 5 }
    ]
  });

  let bondstable = new DataTable('#bonds-table', {
    "searching": false,
    "paging": false,
    "info": false,
    "order": [],
    "columnDefs": [
      { orderable: false, "width": "30%", "targets": 0 },
      { orderable: false, "width": "10%", "targets": 1 },
      { orderable: false, "width": "20%", "targets": 2 },
      { orderable: false, "width": "20%", "targets": 3 },
      { orderable: false, "width": "10%", "targets": 4 },
      { orderable: false, "width": "10%", "targets": 5 }
    ]
  });

  clear_forms();

  setTimeout(function(){refresh_shares()}, 450);
})

function clear_forms() {
  document.querySelectorAll('.form-control').forEach(function(input) {
    input.value = '';
  })
  document.querySelector('#buy-type').value = 'Stock';
  document.querySelector('#buy-currency').value = 'USD';
  document.querySelector('#buy-rating').value = '3';
}

function show_form(formname) {
  if (document.querySelector(`#${formname}-form`).style.display === 'flex') {
    document.querySelectorAll('.form-inline').forEach(function(form) {
      form.style.display = 'none';
    })
  }
  else {
    document.querySelectorAll('.form-inline').forEach(function(form) {
      form.style.display = 'none';
    })
    document.querySelector(`#${formname}-form`).style.display = 'flex';
  }
}

function refresh_shares() {
  fetch('/tickers')
  .then(response => response.json())
  .then(tickers => {
      holdings = tickers;
      document.querySelector('#sell-ticker').innerHTML = '';
      holdings.forEach(function(holding) {
        const element = document.createElement('option');
        element.innerHTML = holding;
        document.querySelector('#sell-ticker').append(element);
      });
  });

  networth = 0;

  fetch('/shares/stock')
  .then(response => response.json())
  .then(shares => {
      document.querySelector('#stocks-table-body').innerHTML = '';
      shares.forEach(function(share) {
        if (share.currency == "USD") {
          networth += share.quantity*share.pricecurrent*usdtorub
        }
        else if (share.currency == "EUR") {
          networth += share.quantity*share.pricecurrent*eurtorub
        }
        else {
          networth += share.quantity*share.pricecurrent
        }
        
        const element = document.createElement('tr');

        if (100*(share.pricecurrent-share.pricebought)/share.pricebought > 0) {
          color = 'green'
        }
        else if (100*(share.pricecurrent-share.pricebought)/share.pricebought < 0) {
          color = 'red'
        }
        else {
          color = 'black'
        }
        element.innerHTML = `<td><a href="share/${share.ticker}">${share.name} (${share.ticker})</a></td><td>${share.quantity}</td><td class="price${share.currency}" id="${share.ticker}">${share.currency} ${share.pricecurrent}</td><td>${share.currency} ${(share.quantity*share.pricecurrent).toFixed(2)}</td><td>${share.rating}/5</td><td class="${color}">${(100*(share.pricecurrent-share.pricebought)/share.pricebought).toFixed(2)}</td>`;
        document.querySelector('#stocks-table-body').append(element);
      });
  });

  fetch('/shares/etf')
  .then(response => response.json())
  .then(shares => {
      document.querySelector('#etfs-table-body').innerHTML = '';
      shares.forEach(function(share) {
        if (share.currency == "USD") {
          networth += share.quantity*share.pricecurrent*usdtorub
        }
        else if (share.currency == "EUR") {
          networth += share.quantity*share.pricecurrent*eurtorub
        }
        else {
          networth += share.quantity*share.pricecurrent
        }

        const element = document.createElement('tr');

        if (100*(share.pricecurrent-share.pricebought)/share.pricebought > 0) {
          color = 'green'
        }
        else if (100*(share.pricecurrent-share.pricebought)/share.pricebought < 0) {
          color = 'red'
        }
        else {
          color = 'black'
        }
        element.innerHTML = `<td><a href="share/${share.ticker}">${share.name} (${share.ticker})</a></td><td>${share.quantity}</td><td class="price${share.currency}" id="${share.ticker}">${share.currency} ${share.pricecurrent}</td><td>${share.currency} ${(share.quantity*share.pricecurrent).toFixed(2)}</td><td>${share.rating}/5</td><td class="${color}">${(100*(share.pricecurrent-share.pricebought)/share.pricebought).toFixed(2)}</td>`;
        document.querySelector('#etfs-table-body').append(element);
      });
  });

  fetch('/shares/bond')
  .then(response => response.json())
  .then(shares => {
      document.querySelector('#bonds-table-body').innerHTML = '';
      shares.forEach(function(share) {
        if (share.currency == "USD") {
          networth += share.quantity*share.pricecurrent*usdtorub
        }
        else if (share.currency == "EUR") {
          networth += share.quantity*share.pricecurrent*eurtorub
        }
        else {
          networth += share.quantity*share.pricecurrent
        }

        const element = document.createElement('tr');
        
        if (100*(share.pricecurrent-share.pricebought)/share.pricebought > 0) {
          color = 'green'
        }
        else if (100*(share.pricecurrent-share.pricebought)/share.pricebought < 0) {
          color = 'red'
        }
        else {
          color = 'black'
        }
        element.innerHTML = `<td><a href="share/${share.ticker}">${share.name} (${share.ticker})</a></td><td>${share.quantity}</td><td class="price${share.currency}" id="${share.ticker}">${share.currency} ${share.pricecurrent}</td><td>${share.currency} ${(share.quantity*share.pricecurrent).toFixed(2)}</td><td>${share.rating}/5</td><td class="${color}">${(100*(share.pricecurrent-share.pricebought)/share.pricebought).toFixed(2)}</td>`;
        document.querySelector('#bonds-table-body').append(element);
      });
  });

  setTimeout(function(){refresh_portfolio()}, 100);
}

function refresh_portfolio() {
  document.querySelector('#networth').innerHTML = `Net Worth: ${networth.toFixed(2)}`;
  dynamics = 100*networth.toFixed(2)/invested;
  if (dynamics > 100) {
    color = 'green'
  }
  else if (dynamics < 100) {
    color = 'red'
  }
  else {
    dynamics = 100
  }
  document.querySelector('#dynamics').innerHTML = `${(dynamics.toFixed(2)-100).toFixed(2)}%`;
  document.querySelector('#dynamics').className = `${color}`;
}

function quote() {
  document.querySelectorAll('.priceUSD').forEach(function(price) {
    fetch(`https://cloud.iexapis.com/stable/stock/${price.id}/quote?token=${token}`)
    .then(response => response.json())
    .then(data => {
      successful.push(price.id);
      fetch(`/share/${price.id}/updateprice`, {
        method: 'POST',
        body: JSON.stringify({
          price: data.latestPrice
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
      .catch((error) => {
        console.log(error)
      })
    });
  })
  setTimeout(function(){refresh_shares()}, 500);
  setTimeout(function(){check_for_success()}, 1000);
}

function check_for_success() {
  document.querySelectorAll('.priceRUB').forEach(function(price) {
    price.className = 'priceRUB orange';
  })
  document.querySelectorAll('.priceUSD').forEach(function(price) {
    if (successful.includes(price.id)) {
      price.className = 'priceUSD';
    }
    else {
      price.className = 'priceUSD orange';
    }
  })
}