import flask
from flask import request
import json
from auth import AuthManager
from messages import MessageManager
from reactions import ReactionsManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per second"]
)
auth_manager = AuthManager()
message_manager = MessageManager()
reactions_manager = ReactionsManager()

@app.route('/', methods=['GET'])
def home():
    return {"erreur": "Chemin invalide, essaye '/messages'"}, 404

@app.route('/tp', methods=['GET'])
def tp():
    return flask.redirect("https://github.com/ue22/backend-alumni", code=301)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json(force=True)
    except Exception:
        return {"erreur": "JSON invalide."}

    pseudo = data.get('pseudo')
    if pseudo is None:
        return {"erreur": "Le parametre 'pseudo' est nul."}, 400
    mdp = data.get('mdp')
    if mdp is None:
        return {"erreur": "Le parametre 'mdp' est nul."}, 400
    
    try:
        auth_manager.register_user(pseudo, mdp)
    except Exception as e:
        return {"erreur": str(e)}, 400
    
    return {"success": True}

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        count = int(request.args.get('count', default=30))
        return message_manager.get_messages(count)
    
    try:
        data = request.get_json(force=True)
    except Exception:
        return {"erreur": "JSON invalide."}
    emetteur = data.get("emetteur")
    if emetteur is None:
        return {"erreur": "Le parametre 'emetteur' est nul."}, 400
    contenu = data.get("contenu")
    if contenu is None:
        return {"erreur": "Le parametre 'contenu' est nul."}, 400
    if len(contenu) > 100:
        return {"erreur": "Le message est trop long."}, 400
    mdp = data.get("mdp")
    verified = mdp is not None
    if verified and not auth_manager.is_valid_user(emetteur, mdp):
            return {"erreur": "Le mot de passe est invalide"}, 400
    
    if "piche" in contenu.lower():
        return {"erreur": "Le message contient un mot interdit."}, 400

    message_manager.add_message(emetteur, contenu, verified)
    return {"success": True}

@app.route('/reactions', methods=['GET', 'POST'])
def reactions():
    if request.method == 'GET':
        msg_id = request.args.get('messageId')
        msg_id_max = request.args.get('messageIdMax')
        if msg_id is None:
            return {"erreur": "Le parametre 'messageId' est nul."}, 400
        try:
            msg_id = int(msg_id)
        except Exception:
            return {"erreur": "Le parametre 'messageId' n'est pas un entier."}, 400
        
        if msg_id_max:
            return reactions_manager.get_many_reactions(msg_id, int(msg_id_max))
        else:
            return reactions_manager.get_reactions(msg_id)
    
    try:
        data = request.get_json(force=True)
    except Exception:
        return {"erreur": "JSON invalide."}
    emetteur = data.get("emetteur")
    if emetteur is None:
        return {"erreur": "Le parametre 'emetteur' est nul."}, 400
    emoji = data.get("emoji")
    if emoji is None:
        return {"erreur": "Le parametre 'emoji' est nul."}, 400
    msg_id = data.get("messageId")
    if msg_id is None:
        return {"erreur": "Le parametre 'messageId' est nul."}, 400
    
    try:
        msg_id = int(msg_id)
    except Exception:
        return {"erreur": "Le parametre 'messageId' n'est pas un entier."}, 400
    
    try:
        reactions_manager.add_reaction(msg_id, emetteur, emoji)
    except Exception as e:
        return {"erreur": str(e)}
    
    return {"success": True}
    
