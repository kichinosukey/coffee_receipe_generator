from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

def create_coffee_recipe(coffee_weight, water_ratio):
    water_amount = coffee_weight * water_ratio
    bloom_water = coffee_weight * 2
    first_pour = water_amount * 0.4
    second_pour = water_amount * 0.67

    data = {
        "ステップ": ["準備", "蒸らし", "透過抽出", "低温浸し", "完成"],
        "詳細": [
            f"コーヒー豆{coffee_weight}g、湯{water_amount}ml、粗挽き（28クリック程度）を用意。",
            f"バルブをクローズにしてお湯を注ぎ、粉全体をしっかり蒸らす（{bloom_water}ml）。",
            f"バルブをオープンにして{first_pour:.0f}mlまで湯を注ぎ、透過抽出を行う（46メソッドと同様）。",
            f"{second_pour:.0f}mlまで湯を追加し、その後湯が落ちきったらバルブを再度クローズする。湯温を70〜80℃まで下げて{water_amount}mlまで注ぎ浸す。",
            "約3分半で抽出完了。バルブをオープンにしてコーヒーをサーバーに落とす。"
        ],
        "時間目安": ["-", "0:00 - 0:30", "0:30 - 1:30", "1:30 - 3:00", "3:00 - 3:30"]
    }

    return pd.DataFrame(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_recipe', methods=['GET'])
def create_recipe():
    coffee_weight = float(request.args.get('coffee_weight', 0))
    water_ratio = float(request.args.get('water_ratio', 0))
    
    recipe_df = create_coffee_recipe(coffee_weight, water_ratio)
    
    return jsonify(recipe_df.to_dict(orient='split'))

if __name__ == '__main__':
    app.run(debug=True)