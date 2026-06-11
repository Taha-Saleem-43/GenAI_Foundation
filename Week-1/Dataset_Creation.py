import json
import random

# Sample themes for variety
themes = [
    "coffee promo", "gym motivation", "travel ad", "tech startup",
    "AI education", "food brand", "fashion sale", "real estate",
    "mobile app launch", "fitness coaching"
]

texts = {
    "coffee promo": [
        "Start your day with fresh coffee",
        "Brewed from premium beans",
        "Taste the richness in every sip"
    ],
    "gym motivation": [
        "Push your limits",
        "No excuses, just results",
        "Train like a champion"
    ],
    "travel ad": [
        "Explore the world",
        "Find your adventure",
        "Travel beyond limits"
    ],
    "tech startup": [
        "Innovating the future",
        "AI-powered solutions",
        "Build smarter systems"
    ],
    "AI education": [
        "Learn AI the easy way",
        "Master machine learning",
        "Future belongs to AI"
    ],
    "food brand": [
        "Delicious in every bite",
        "Made with fresh ingredients",
        "Taste the difference"
    ],
    "fashion sale": [
        "New arrivals now live",
        "Style that defines you",
        "Flat 50% off today"
    ],
    "real estate": [
        "Find your dream home",
        "Luxury living made easy",
        "Invest in your future"
    ],
    "mobile app launch": [
        "Your app, your power",
        "Launch smarter apps",
        "Experience innovation"
    ],
    "fitness coaching": [
        "Transform your body",
        "Personalized training plans",
        "Achieve your goals"
    ]
}

image_urls = [
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg",
    "https://example.com/img3.jpg",
    "https://example.com/img4.jpg",
    "https://example.com/img5.jpg"
]

def generate_scene(theme):
    return {
        "text": random.choice(texts[theme]),
        "duration": random.randint(2, 4),
        "image_url": random.choice(image_urls)
    }

def generate_example():
    theme = random.choice(themes)

    scenes = [generate_scene(theme) for _ in range(random.randint(3, 5))]

    user_prompt = f"Create a 10 second {theme} video"

    assistant_output = {
        "title": theme.title(),
        "width": 1920,
        "height": 1080,
        "scenes": scenes
    }

    return {
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            },
            {
                "role": "assistant",
                "content": json.dumps(assistant_output)
            }
        ]
    }

# Generate 100 examples
dataset = [generate_example() for _ in range(100)]

# Save to JSONL file
with open("creatomate_train.jsonl", "w") as f:
    for item in dataset:
        f.write(json.dumps(item) + "\n")

print("100-example dataset generated: creatomate_train.jsonl")