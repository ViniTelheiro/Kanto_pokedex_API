from distutils.log import error
from email import message
import requests
import cv2
import json

    #method to get all pokemons names:
def pokedex():
    request = requests.get('https://pokeapi.co/api/v2/pokedex/kanto')
    data = request.json()
    names = []
    for pokemon in data['pokemon_entries']:
        names.append(pokemon['pokemon_species']['name'])
    return names


class Pokemon():
    def __init__(self, name:str) -> None:       
        first_gen = pokedex()
        name = name.strip().lower()
        
        if not name in first_gen:
            error_msg = f"can't find {name} in pokedex. Try to run print(pokedex()) to see the avaliable pokemons."
            raise Exception(error_msg)
        
        # set name and number
        self.name = name.capitalize()
        self.number = first_gen.index(name)
        
        request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/')
        data = request.json()
        
        #set private atribute
        self.__data = data
        
        # set types
        types = []
        for data_types in data['types']:
            types.append(data_types['type']['name'])

        self.types = types
        
        #set possible abilities
        abilities = []
        for data_abilities in data['abilities']:
            abilities.append(data_abilities['ability']['name'])
        
        self.ability = abilities
    
    def show_info(self) -> None:
        print(f'Nº.{self.number}-{self.name}\t type: {", ".join(self.types)}\t abilities: {", ".join(self.ability)}')
    
    def get_location(self):
        area = self.__data['location_area_encounters']
        request = requests.get(area)
        area = request.json()
        for data in area:
            #print(data['version_details'][-1]['version']['name'])        
            print(data['version_details'][-1])        
    
    def get_possible_moves(self) -> None:
        all_moves = []
        
        for move in self.__data['moves']:
            for gen in move['version_group_details']:
                if 'red' in gen['version_group']['name'] or 'blue' in gen['version_group']['name']:
                    if move['move']['name'] not in all_moves:
                        all_moves.append(move['move']['name'])
        print(all_moves)
    
    def set_moves(self, moves:list):
        if len(moves) > 4:
            raise Exception('pokemons cannot learn more than 4 moves')
        if len(moves) == 0:
            raise Exception('Pokemons must learn at least one move')
        possible_moves = []
        
        for move in self.__data['moves']:
            for gen in move['version_group_details']:
                if 'red' in gen['version_group']['name'] or 'blue' in gen['version_group']['name']:
                    if move['move']['name'] not in possible_moves:
                        possible_moves.append(move['move']['name'])
        moveset = []
        for move in moves:
            if move not in possible_moves:
                message = f'{self.name} cannot learn the move {move}! To see what moves {self.name} can learn in Kanto run get_possible_moves method.'
                raise Exception(message)
            
            if move in moveset:
                continue
            else:
                moveset.append(str(move).lower().strip())

        self.moveset = moveset
        