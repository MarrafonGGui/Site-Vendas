from flask import Blueprint, render_template, url_for, request
from model import db, Venda, Produto, Cliente

vendassite = Blueprint('vendassite', __name__)

@vendassite.route('/')
def home_vendas():
    return render_template('vendas/vendas.html')

@vendassite.route('/efetuar', methods=["GET","POST"])
def efetuar_vendas():
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        id_produto = request.form.get("id_produto")
        quantidade = int(request.form.get("quantidade"))

        produto = Produto.query.get(id_produto)

        if not produto:
            return "Produto não encontrado"

        if produto.quantidade < quantidade:
            return "Estoque insuficiente"

        venda = Venda(
            id_cliente=id_cliente,
            id_produto=id_produto,
            quantidade=quantidade,
            preco=produto.preco,
            preco_total=produto.preco * quantidade
        )

        # desconta do estoque
        produto.quantidade -= quantidade

        db.session.add(venda)
        db.session.commit()

        return render_template("vendas/fimvenda.html", venda=venda)
    
    clientes = Cliente.query.all()
    produtos = Produto.query.all()

    return render_template("vendas/efetvenda.html", clientes=clientes, produtos=produtos)


@vendassite.route("/lista")
def listar_vendas():
    vendas = Venda.query.all()
    return render_template("vendas/listvenda.html", vendas=vendas)