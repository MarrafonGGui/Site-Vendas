function validarFormulario() {
    const nome = document.getElementById("nome").value.toLowerCase();
    const preco = document.getElementById("preco").value;

    const existe = produtosExistentes.includes(nome);

    if (!existe && preco <= 0) {
        alert("Produto novo precisa ter preço maior que zero!");
        return false;
    }

    return true;
}