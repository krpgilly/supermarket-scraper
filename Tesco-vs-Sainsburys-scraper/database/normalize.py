def normalize_price(price_str, weight_str):
    """
    Convert raw price + weight strings into price per 100g.
    Handles 'g' and 'kg' variations smoothly.
    """
    try:
        if "£" in price_str:
            price = float(price_str.replace("£", "").strip())
        elif "p" in price_str:
            price = float(price_str.replace("p", "").strip()) / 100
        else:
            print(f"Unknown price format: {price_str}")
            return None

        weight_clean = weight_str.lower().strip()
        
        if "kg" in weight_clean:
            weight = float(weight_clean.replace("kg", "").strip())
            weight_grams = weight * 1000
        elif "mg" in weight_clean:
            weight = float(weight_clean.replace("mg", "").strip())
            weight_grams = weight / 1000
        elif "g" in weight_clean:
            weight_grams = float(weight_clean.replace("g", "").strip())
            
        else:
            print(f"Unknown weight format: {weight_str}")
            return None

        if weight_grams == 0:
            print(f"Weight cannot be zero: {weight_str}") 
            return None
        
        price_per_100g = (price / weight_grams) * 100
        return round(price_per_100g, 3)
        
    except Exception as e:
        print(f"Error normalising price ({price_str}) and weight ({weight_str}):", e)
        return None

def normalize_unit_price(unit_price_str):
    try:
        price = unit_price_str.replace("£", "").replace("(", "").replace(")", "").replace(" ", "").strip()

        if "/100g" in price:
            price = float(price.replace("/100g", "").strip())
            return round(price, 3)
        elif "/kg" in price:
                price = float(price.replace("/kg", "").strip()) / 10
                return round(price, 3)
        else:
            print(f"Unknown unit price format: {unit_price_str}")
            return None

    except Exception as e:
        print(f"Error normalising unit price ({unit_price_str}):", e)
        return None
