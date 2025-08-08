import re
import sys

PHYSICAL_TYPES = {
    'TYPE_NORMAL', 'TYPE_FIGHTING', 'TYPE_FLYING', 'TYPE_POISON', 
    'TYPE_GROUND', 'TYPE_ROCK', 'TYPE_BUG', 'TYPE_GHOST', 'TYPE_STEEL'
}

SPECIAL_TYPES = {
    'TYPE_FIRE', 'TYPE_WATER', 'TYPE_ELECTRIC', 'TYPE_GRASS', 
    'TYPE_ICE', 'TYPE_PSYCHIC', 'TYPE_DRAGON', 'TYPE_DARK'
}

STATUS_MOVES = {
    'EFFECT_TELEPORT', 'EFFECT_SLEEP', 'EFFECT_TOXIC', 'EFFECT_PARALYZE',
    'EFFECT_BURN', 'EFFECT_FREEZE', 'EFFECT_CONFUSE', 'EFFECT_ATTRACT',
    'EFFECT_DEFENSE_UP', 'EFFECT_ATTACK_UP', 'EFFECT_SPEED_UP', 
    'EFFECT_SPECIAL_ATTACK_UP', 'EFFECT_SPECIAL_DEFENSE_UP', 'EFFECT_ACCURACY_UP',
    'EFFECT_EVASION_UP', 'EFFECT_DEFENSE_DOWN', 'EFFECT_ATTACK_DOWN',
    'EFFECT_SPEED_DOWN', 'EFFECT_SPECIAL_ATTACK_DOWN', 'EFFECT_SPECIAL_DEFENSE_DOWN',
    'EFFECT_ACCURACY_DOWN', 'EFFECT_EVASION_DOWN', 'EFFECT_HAZE', 'EFFECT_BIDE',
    'EFFECT_RAMPAGE', 'EFFECT_ROAR', 'EFFECT_MULTI_HIT', 'EFFECT_CONVERSION',
    'EFFECT_RESTORE_HP', 'EFFECT_LIGHT_SCREEN', 'EFFECT_REFLECT', 'EFFECT_POISON',
    'EFFECT_PARALYZE', 'EFFECT_SUBSTITUTE', 'EFFECT_MIMIC', 'EFFECT_METRONOME',
    'EFFECT_LEECH_SEED', 'EFFECT_SPLASH', 'EFFECT_DISABLE', 'EFFECT_MIST',
    'EFFECT_FOCUS_ENERGY', 'EFFECT_TRANSFORM', 'EFFECT_DEFENSE_UP_2',
    'EFFECT_ATTACK_UP_2', 'EFFECT_SPEED_UP_2', 'EFFECT_SPECIAL_ATTACK_UP_2',
    'EFFECT_SPECIAL_DEFENSE_UP_2', 'EFFECT_DEFENSE_DOWN_2', 'EFFECT_ATTACK_DOWN_2',
    'EFFECT_SPEED_DOWN_2', 'EFFECT_SPECIAL_ATTACK_DOWN_2', 'EFFECT_SPECIAL_DEFENSE_DOWN_2'
}

def categorize_move(move_data):
    power_match = re.search(r'\.power = (\d+)', move_data)
    power = int(power_match.group(1)) if power_match else 0
    
    type_match = re.search(r'\.type = (TYPE_\w+)', move_data)
    move_type = type_match.group(1) if type_match else 'TYPE_NORMAL'
    
    effect_match = re.search(r'\.effect = (EFFECT_\w+)', move_data)
    effect = effect_match.group(1) if effect_match else 'EFFECT_HIT'
    
    has_contact = 'FLAG_MAKES_CONTACT' in move_data
    
    if power == 0 or effect in STATUS_MOVES:
        return 'MOVE_CATEGORY_STATUS'
    
    if has_contact or move_type in PHYSICAL_TYPES:
        return 'MOVE_CATEGORY_PHYSICAL'
    
    if move_type in SPECIAL_TYPES:
        return 'MOVE_CATEGORY_SPECIAL'
    
    if move_type in PHYSICAL_TYPES:
        return 'MOVE_CATEGORY_PHYSICAL'
    else:
        return 'MOVE_CATEGORY_SPECIAL'

def process_battle_moves_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    move_pattern = r'(\[MOVE_\w+\] =\s*\{[^}]+\})'
    moves = re.findall(move_pattern, content, re.DOTALL)
    
    print(f"founded moves: {len(moves)}")
    
    for move_data in moves:
        if '.category = ' in move_data:
            continue
            
        category = categorize_move(move_data)
        
        new_move_data = move_data.rstrip().rstrip('}').rstrip(',')
        new_move_data += f',\n        .category = {category},\n    }}'
        
        content = content.replace(move_data, new_move_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("fixed")

if __name__ == '__main__':
    filename = 'src/data/battle_moves.h'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    process_battle_moves_file(filename)
