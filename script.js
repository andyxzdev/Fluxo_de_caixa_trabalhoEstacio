document.getElementById("transaction-form").addEventListener("submit", addTransaction);

async function addTransaction(event) {
    event.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const type = document.getElementById("type").value;

    const transaction = { descricao: description, valor: amount };

    const endpoint = type === "income" ? "receita" : "despesa";
    const response = await fetch(`http://localhost:5000/api/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(transaction),
    });

    if (response.ok) {
        fetchFluxoCaixa();
    }
}

async function fetchFluxoCaixa() {
    const response = await fetch("http://localhost:5000/api/fluxo_caixa");
    const fluxoCaixa = await response.json();

    displayTransactions(fluxoCaixa.receitas, fluxoCaixa.despesas);
    updateBalance(fluxoCaixa.saldo);
}

function displayTransactions(receitas, despesas) {
    const list = document.getElementById("transaction-list");
    list.innerHTML = "";

    receitas.forEach((receita) => {
        const listItem = document.createElement("li");
        listItem.classList.add("transaction-item", "income");
        listItem.innerHTML = `${receita.descricao} - R$ ${receita.valor.toFixed(2)}`;
        list.appendChild(listItem);
    });

    despesas.forEach((despesa) => {
        const listItem = document.createElement("li");
        listItem.classList.add("transaction-item", "expense");
        listItem.innerHTML = `${despesa.descricao} - R$ ${despesa.valor.toFixed(2)}`;
        list.appendChild(listItem);
    });
}

function updateBalance(saldo) {
    document.getElementById("balance").textContent = saldo.toFixed(2);
}

fetchFluxoCaixa();
