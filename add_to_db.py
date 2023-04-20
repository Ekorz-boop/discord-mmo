from server import db, CharacterClass, Ability

classes = [
    {
        'name': 'Warrior',
        'description': 'A strong and resilient melee combatant.',
        'starting_hp': 10,
        'hp_per_level': 6
    },
    {
        'name': 'Wizard',
        'description': 'A master of the arcane arts, specializing in powerful spells.',
        'starting_hp': 6,
        'hp_per_level': 4
    },
    {
        'name': 'Druid',
        'description': 'A spellcaster in tune with nature, able to shapeshift and control the elements.',
        'starting_hp': 8,
        'hp_per_level': 5
    },
    {
        'name': 'Ranger',
        'description': 'A skilled archer and hunter, adept at tracking and surviving in the wild.',
        'starting_hp': 8,
        'hp_per_level': 5
    },
    {
        'name': 'Paladin',
        'description': 'A holy warrior, combining melee prowess with divine magic.',
        'starting_hp': 10,
        'hp_per_level': 6
    },
]

abilities = [
    # Warrior abilities
    {
        'name': 'Strike',
        'description': 'A powerful melee attack.',
        'effect': 'Deal physical damage.',
        'class_id': 1
    },
    {
        'name': 'Taunt',
        'description': 'Taunt enemies, forcing them to attack you.',
        'effect': 'Enemies focus on the warrior.',
        'class_id': 1
    },
    {
        'name': 'Charge',
        'description': 'Charge at an enemy, closing the gap.',
        'effect': 'Move to an enemy and deal damage.',
        'class_id': 1
    },
    {
        'name': 'Defend',
        'description': 'Take a defensive stance, reducing damage taken.',
        'effect': 'Decrease damage taken.',
        'class_id': 1
    },

    # Wizard abilities
    {
        'name': 'Fireball',
        'description': 'Launch a ball of fire at enemies.',
        'effect': 'Deal fire damage to enemies in an area.',
        'class_id': 2
    },
    {
        'name': 'Frostbolt',
        'description': 'Shoot a bolt of frost at an enemy.',
        'effect': 'Deal cold damage and slow the enemy.',
        'class_id': 2
    },
    {
        'name': 'Teleport',
        'description': 'Instantly teleport to a nearby location.',
        'effect': 'Move to a chosen location.',
        'class_id': 2
    },
    {
        'name': 'Arcane Barrier',
        'description': 'Create a magical barrier that absorbs damage.',
        'effect': 'Absorb a fixed amount of damage.','class_id': 2
    },


    # Druid abilities
    {
        'name': 'Healing Touch',
        'description': 'Heal a target with the power of nature.',
        'effect': 'Heal a friendly target.',
        'class_id': 3
    },
    {
        'name': 'Entangling Roots',
        'description': 'Root an enemy in place, preventing movement.',
        'effect': 'Immobilize an enemy.',
        'class_id': 3
    },
    {
        'name': 'Moonfire',
        'description': 'Call down a beam of lunar energy to damage an enemy.',
        'effect': 'Deal damage over time.',
        'class_id': 3
    },
    {
        'name': 'Shapeshift',
        'description': 'Transform into various forms to adapt to different situations.',
        'effect': 'Gain different abilities and stats.',
        'class_id': 3
    },

    # Ranger abilities
    {
        'name': 'Aimed Shot',
        'description': 'Carefully aim your shot for increased damage.',
        'effect': 'Deal physical damage.',
        'class_id': 4
    },
    {
        'name': 'Volley',
        'description': 'Fire multiple arrows at once to damage multiple enemies.',
        'effect': 'Deal physical damage to enemies in an area.',
        'class_id': 4
    },
    {
        'name': 'Evade',
        'description': 'Quickly dodge out of harm\'s way.',
        'effect': 'Avoid the next incoming attack.',
        'class_id': 4
    },
    {
        'name': 'Pet',
        'description': 'Summon a pet to fight alongside you.',
        'effect': 'Summon a pet with its own abilities.',
        'class_id': 4
    },

    # Paladin abilities
    {
        'name': 'Smite',
        'description': 'Strike an enemy with holy power.',
        'effect': 'Deal holy damage.',
        'class_id': 5
    },
    {
        'name': 'Lay on Hands',
        'description': 'Heal a target by laying your hands upon them.',
        'effect': 'Heal a friendly target.',
        'class_id': 5
    },
    {
        'name': 'Aegis',
        'description': 'Shield an ally, absorbing damage.',
        'effect': 'Absorb a fixed amount of damage for an ally.',
        'class_id': 5
    },
    {
        'name': 'Consecrate',
        'description': 'Consecrate the ground around you, damaging enemies and empowering allies.',
        'effect': 'Deal holy damage to enemies and increase ally stats.',
        'class_id': 5
    },
]


for character_class in classes:
    new_class = CharacterClass(**character_class)
    db.session.add(new_class)

for ability in abilities:
    new_ability = Ability(**ability)
    db.session.add(new_ability)

db.session.commit()





