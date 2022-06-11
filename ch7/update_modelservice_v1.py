import redis
from flask import g

@app.route('/update-model', methods=['POST'])
def update_model():
    _cache = get_cache()
    new_model_path = request.args.get('model_path')
    load_model(new_model_path)
    _cache.set('model_hash', model.hash)
    _cache.set('model_location', path)
return jsonify({'状态': '模型更新成功!'})

@app.teardown_request
def check_cache(ctx):
    _cache = get_cache()
    global model
    cached_hash = _cache.get('model_hash')
    if model.hash != cached_hash:
        model_location = _cache.get('model_location')
        load_model(model_location)
def get_cache():
    if 'cache' not in g:
        g.cache = redis.Redis()
    return g.cache

