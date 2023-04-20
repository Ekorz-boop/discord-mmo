'''server.py'''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hp = db.Column(db.Integer, nullable=False, default=100)
    attack = db.Column(db.Integer, nullable=False, default=10)
    defense = db.Column(db.Integer, nullable=False, default=5)
    money = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False, default=1)
    arrival_time = db.Column(db.DateTime, nullable=True)
    dungeon_id = db.Column(db.Integer, db.ForeignKey('dungeon.id'), nullable=True)
    current_room = db.Column(db.Integer, nullable=True)
    character_class_id = db.Column(db.Integer, db.ForeignKey('character_class.id'), nullable=True)
    

    inventory = db.relationship('Item', backref='player', lazy=True)
    abilities = db.relationship('PlayerAbility', backref='player', lazy=True)
    character_class = db.relationship('CharacterClass', lazy=True)

    def __repr__(self):
        return f'<Player {self.username}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Item {self.name}>'

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Location {self.name}>'

class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    method = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes

    def __repr__(self):
        return f'<Travel {self.from_location_id}:{self.to_location_id}>'

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    reward_money = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Monster {self.name}>'

class Dungeon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Dungeon {self.id}>'

class DungeonRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dungeon_id = db.Column(db.Integer, db.ForeignKey('dungeon.id'), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey('monster.id'), nullable=False)

    def __repr__(self):
        return f'<DungeonRoom {self.id}>'
    
class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    effect = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('character_class.id'), nullable=True)

    character_class = db.relationship('CharacterClass', lazy=True)

    def __repr__(self):
        return f'<Ability {self.name}>'


class PlayerAbility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'), nullable=False)
    cooldown_end = db.Column(db.DateTime, nullable=True)

    ability = db.relationship('Ability', lazy=True)

    def __repr__(self):
        return f'<PlayerAbility {self.ability.name}>'
    

class CharacterClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    starting_hp = db.Column(db.Integer, nullable=False)
    hp_per_level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<CharacterClass {self.name}>'


def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/api/player', methods=['POST'])
def create_player():
    username = request.form.get('username')
    existing_player = Player.query.filter_by(username=username).first()
    if existing_player:
        return jsonify({"error": "A player with that username already exists."}), 400
    player = Player(username=username)
    db.session.add(player)
    db.session.commit()
    return jsonify({"player_id": player.id})

@app.route('/api/player', methods=['GET'])
def get_player():
    player_id = request.args.get('player_id')
    player = Player.query.get(player_id)
    if player:
        return jsonify({"username": player.username, "hp": player.hp, "attack": player.attack, "defense": player.defense, "money": player.money, "level": player.level})
    else:
        return jsonify({"error": "Player not found."}), 404

@app.route('/api/player/inventory', methods=['GET'])
def get_inventory():
    player_id = request.args.get('player_id')
    player = Player.query.get(player_id)
    if player:
        inventory = [{"name": item.name, "quantity": item.quantity} for item in player.inventory]
        return jsonify({"inventory": inventory})
    else:
        return jsonify({"error": "Player not found."}), 404

@app.route('/api/trade', methods=['POST'])
def trade_items():
    from_player_id = request.form.get('from_player_id')
    to_player_id = request.form.get('to_player_id')
    item_name = request.form.get('item_name')
    quantity = int(request.form.get('quantity', 1))

    from_player = Player.query.get(from_player_id)
    to_player = Player.query.get(to_player_id)

    if not from_player or not to_player:
        return jsonify({"error": "Invalid player ID(s)."}), 400

    from_item = Item.query.filter_by(player_id=from_player_id, name=item_name).first()

    if not from_item or from_item.quantity < quantity:
        return jsonify({"error": "Insufficient item quantity."}), 400

    to_item = Item.query.filter_by(player_id=to_player_id, name=item_name).first()

    if to_item:
        to_item.quantity += quantity
    else:
        to_item = Item(player_id=to_player_id, name=item_name, quantity=quantity)
        db.session.add(to_item)

    from_item.quantity -= quantity
    if from_item.quantity == 0:
        db.session.delete(from_item)

    db.session.commit()
    return jsonify({"message": "Trade successful."})

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify({"locations": [{"id": location.id, "name": location.name, "description": location.description} for location in locations]})

@app.route('/api/travel', methods=['POST'])
def travel():
    player_id = request.form.get('player_id')
    to_location_id = request.form.get('to_location_id')
    travel_method = request.form.get('travel_method')

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Invalid player ID."}), 400

    travel_entry = Travel.query.filter_by(from_location_id=player.location_id, to_location_id=to_location_id, method=travel_method).first()
    if not travel_entry:
        return jsonify({"error": "Invalid travel method or location."}), 400

    player.location_id = to_location_id
    player.arrival_time = datetime.utcnow() + timedelta(minutes=travel_entry.duration)
    db.session.commit()

    return jsonify({"message": f"Traveling to location {to_location_id} using {travel_method}. Estimated arrival time: {player.arrival_time} UTC."})

def resolve_combat(player, monster):
    player_hp = player.hp
    monster_hp = monster.hp

    while player_hp > 0 and monster_hp > 0:
        monster_hp -= max(0, player.attack - monster.defense)
        if monster_hp > 0:
            player_hp -= max(0, monster.attack - player.defense)

    return player_hp > 0

@app.route('/api/dungeon/enter', methods=['POST'])
def enter_dungeon():
    player_id = request.form.get('player_id')
    location_id = request.form.get('location_id')
    difficulty = int(request.form.get('difficulty', 1))
    num_rooms = int(request.form.get('num_rooms', 5))

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Invalid player ID."}), 400

    dungeon = Dungeon(location_id=location_id, difficulty=difficulty)
    db.session.add(dungeon)
    db.session.commit()

    for i in range(num_rooms):
        monster = random.choice(Monster.query.all())
        dungeon_room = DungeonRoom(dungeon_id=dungeon.id, monster_id=monster.id)
        db.session.add(dungeon_room)

    db.session.commit()

    player.dungeon_id = dungeon.id
    player.current_room = 1
    db.session.commit()

    return jsonify({"message": f"You have entered a dungeon with {num_rooms} rooms.", "dungeon_id": dungeon.id})

@app.route('/api/player/abilities', methods=['GET'])
def get_abilities():
    player_id = request.args.get('player_id')
    player = Player.query.get(player_id)
    if player:
        abilities = [{"name": pa.ability.name, "description": pa.ability.description, "effect": pa.ability.effect, "cooldown_end": pa.cooldown_end} for pa in player.abilities]
        return jsonify({"abilities": abilities})
    else:
        return jsonify({"error": "Player not found."}), 404
    
@app.route('/api/character_classes', methods=['GET'])
def get_character_classes():
    character_classes = CharacterClass.query.all()
    return jsonify({"character_classes": [{"id": cclass.id, "name": cclass.name, "description": cclass.description} for cclass in character_classes]})

@app.route('/api/player/set_class', methods=['POST'])
def set_character_class():
    player_id = request.form.get('player_id')
    character_class_id = request.form.get('character_class_id')

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found."}), 404

    character_class = CharacterClass.query.get(character_class_id)
    if not character_class:
        return jsonify({"error": "Character class not found."}), 404

    player.character_class_id = character_class_id
    db.session.commit()

    return jsonify({"message": f"Character class set to {character_class.name}."})


@app.route('/api/abilities', methods=['GET'])
def get_abilities_by_class():
    class_id = request.args.get('class_id')
    abilities = Ability.query.filter_by(class_id=class_id).all()
    return jsonify({"abilities": [{"id": ability.id, "name": ability.name, "description": ability.description, "effect": ability.effect} for ability in abilities]})


@app.route('/api/combat/use_ability', methods=['POST'])
def use_ability():
    combat_id = request.form.get('combat_id')
    player_id = request.form.get('player_id')
    ability_id = request.form.get('ability_id')

    combat = Combat.query.get(combat_id)
    if not combat:
        return jsonify({"error": "Combat not found."}), 404

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found."}), 404

    ability = Ability.query.get(ability_id)
    if not ability:
        return jsonify({"error": "Ability not found."}), 404

    # Implement your ability effects here, e.g., deal damage, heal, etc.
    # ...

    combat.ability_id = ability_id
    db.session.commit()

    return jsonify({"message": f"{player.name} used {ability.name}."})
def apply_damage_ability(target, damage):
    target.hp -= damage
    if target.hp < 0:
        target.hp = 0
    db.session.commit()


def apply_healing_ability(target, healing):
    target.hp += healing
    if target.hp > target.max_hp:
        target.hp = target.max_hp
    db.session.commit()


def apply_aoe_damage_ability(targets, damage):
    for target in targets:
        apply_damage_ability(target, damage)
