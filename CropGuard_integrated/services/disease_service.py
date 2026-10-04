
def get_disease_info(disease):
    fallback = {
        "what": "The AI detected a pattern associated with this disease. Confirm the diagnosis locally before applying treatment.",
        "cause": "Disease development depends on the pathogen, crop condition and environmental conditions.",
        "symptoms": ["Visible changes in leaf appearance", "Affected areas may expand over time"],
        "spread": "It can spread between plants through environmental conditions and movement of affected plant material.",
        "conditions": "Humidity, leaf wetness and crop stress can increase disease pressure for many diseases.",
        "action": "Monitor affected zones closely and follow locally approved agricultural treatment guidance.",
        "prevention": ["Inspect the field regularly", "Maintain good airflow", "Manage infected plant material appropriately"],
        "reinspect": "Inspect the affected zone within 24 to 48 hours.",
    }

    data = {
        "Corn Late/Leaf Blight": {
            "what": "A fungal-like disease that can damage corn leaves, stems and vegetable and spread quickly under favorable conditions.",
            "cause": "It is associated with Phytophthora infestans and is strongly influenced by cool, wet and humid conditions.",
            "symptoms": ["Dark irregular lesions on leaves", "Rapid browning or collapse of affected tissue", "Dark lesions may occur on stems or fruit"],
            "spread": "Spores can move between plants through water, wind and infected plant material.",
            "conditions": "Extended leaf wetness, humidity and suitable temperatures can increase disease pressure.",
            "action": "Prioritize high-severity zones and follow locally approved treatment guidance from an agricultural professional.",
            "prevention": ["Inspect lower foliage regularly", "Improve airflow", "Avoid prolonged leaf wetness", "Manage infected material carefully"],
            "reinspect": "Reinspect high-severity zones within 24 hours.",
        },
        "Early Blight": {
            "what": "A common corn disease that produces spots on leaves and can reduce healthy leaf area.",
            "cause": "It is commonly associated with Alternaria species and is favored by leaf wetness and plant stress.",
            "symptoms": ["Brown spots with concentric rings", "Yellowing around older lesions", "Progressive loss of affected leaf tissue"],
            "spread": "Spores can spread through rain splash, irrigation, wind and infected plant debris.",
            "conditions": "Leaf wetness, humidity and plant stress can increase disease pressure.",
            "action": "Monitor affected zones closely, improve airflow and follow locally approved treatment recommendations.",
            "prevention": ["Avoid prolonged leaf wetness", "Maintain spacing and airflow", "Manage infected debris", "Rotate crops where practical"],
            "reinspect": "Reinspect affected zones within 48 hours.",
        },
    }
    return data.get(disease, fallback)
