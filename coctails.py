import requests
import random

def drink_maker(ingredients, image_url):
    return{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ingredients#"*Margarita*\nIngredients:\nTequila - 1 1/2 oz\nTriple sec - 1/2 oz\nLime juice - 1 oz\nSalt"
        },
        "accessory": {
            "type": "image",
            "alt_text": "drink",
            "image_url": image_url#"https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg"
        }
    }

def howto_maker(howto):
    return{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": howto#"*How to:*\nRub the rim of the glass with the lime slice to make the salt stick to it. Take care to moisten only the outer rim and sprinkle the salt on it. The salt should present to the lips of the imbiber and never mix into the cocktail. Shake the other ingredients with ice, then carefully pour into the glass.\nGlass: Cocktail glass"
        }
    }

divider_json = {"type": "divider"}

def response_data_combiner(data):
    drinks = []
    for drink in data:
        image_url = drink['strDrinkThumb']
        ingredients = "*{}*\nIngredients:\n".format(drink['strDrink'])
        i = 1
        while(True):
            ingredients += drink['strIngredient%i' % i]
            if drink['strMeasure%i' % i] != None:
                ingredients += ' - ' + drink['strMeasure%i' % i]
            ingredients += '\n'
            i += 1
            if i > 15 :
                break
            if drink['strIngredient%i' % i] == None:
                break
        howto = "*How to*:\n" + drink['strInstructions']
        drinks.append(drink_maker(ingredients, image_url))
        drinks.append(howto_maker(howto))
        drinks.append(divider_json)
    return drinks

def get_named_cocktail(name):
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=%s' % name)
    data = response.json()
    return response_data_combiner(data['drinks'])
    
    
def get_random_drink():
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    data = response.json()
    return response_data_combiner(data['drinks'])

def get_drinks_by_id(id_list):
    all_drinks = []
    for drink_id in id_list:
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=%s' % drink_id['idDrink'])
        data = response.json()
        all_drinks.append(data['drinks'][0])
    return response_data_combiner(all_drinks)

def get_by_ingredient(name):
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s' % name)
    data = response.json()
    random.shuffle(data['drinks'])
    if len(data['drinks']) < 3:
        coctails_to_get = data['drinks'][:len(data['drinks'])]
    else:
        coctails_to_get = data['drinks'][:3]
    
    return get_drinks_by_id(coctails_to_get)



#print(get_by_ingredient('gin'))