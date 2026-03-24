from flask import Blueprint, render_template, request, redirect, url_for
from model import db, Cliente

clientesite = Blueprint('clientesite', __name__)

@clientesite.route("/")
def home_cliente():
    return render_template('cliente/cliente.html')


@clientesite.route("/cadastro", methods=["GET", "POST"])
def cadastro_cliente():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        email = request.form.get("email")

        cpf = ''.join(filter(str.isdigit, cpf))

        if not validar_cpf(cpf):
            return "CPF inválido"

        existe = Cliente.query.filter_by(cpf=cpf).first()
        if existe:
            return "CPF já cadastrado"

        cliente = Cliente(cpf=cpf, nome=nome, email=email)
        db.session.add(cliente)
        db.session.commit()

        return redirect(url_for("clientesite.cadastro_cliente"))
    return render_template('cliente/cadcliente.html')


@clientesite.route("/lista")
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('cliente/listcliente.html', clientes=clientes)

    
    

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10

    # Segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{d1}{d2}"
