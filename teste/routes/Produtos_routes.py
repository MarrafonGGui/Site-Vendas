from flask import Blueprint, render_template, url_for, request, redirect
from model import db, Produto

produtossite = Blueprint('produtossite', __name__)

@produtossite.route('/', methods=["GET", "POST"])
def home_produtos():
    return render_template('produto/produtos.html')


@produtossite.route('/lista')
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produto/listproduto.html', produtos=produtos)

@produtossite.route('/cadastro', methods=["GET", "POST"])
def cadastro_produtos():
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = int(request.form.get("quantidade"))

        # verifica se já existe
        produto_existente = Produto.query.filter_by(nome_produto=nome).first()
        if produto_existente:
            # soma quantidade
            produto_existente.quantidade += quantidade

            # atualizar preço
            if float(preco) < 0:
                return "Preço inválido"
            if produto_existente.preco != float(preco) and float(preco) != 0:
                produto_existente.preco = float(preco)

        else:
            # cria novo produto
            produto = Produto(
                nome_produto=nome,
                preco=float(preco),
                quantidade=quantidade
            )
            db.session.add(produto)
        db.session.commit()

        return redirect(url_for("produtossite.cadastro_produtos"))
    lista_produtos = Produto.query.all()

    return render_template('produto/cadproduto.html', produtos=lista_produtos)