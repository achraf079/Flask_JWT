from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from flask import request
from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "ma_cle"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Ma clée privée
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok..
# La fonction create_access_token() est utilisée pour générer un jeton JWT..


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username == "admin_user" and password == "admin_pass":
        role = "admin"
    elif username == "regular_user" and password == "user_pass":
        role = "user"
    else
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity={"username": username, "role": role})
    
    return jsonify(
        access_token=access_token
    )

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"msg": "Accès refusé : rôle admin requis"}), 403
    return jsonify({"msg": f"Bienvenue {identity['username']}, vous êtes administrateur."})


# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
                                                                                                               
if __name__ == "__main__":
  app.run(debug=True)
