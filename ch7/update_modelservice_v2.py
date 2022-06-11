import redis
from flask import g

@app.route('/update-model', methods=['POST'])
def update_model():
    _cache = get_cache()
    new_path = request.args.get('model_path')
    busy_signal = int(_cache.get('busy_signal'))
    if not busy_signal:
        _cache.set('busy_signal', 1)
        load_model(new_path, _cache)
        _cache.set('busy_signal', 0)
    return jsonify({'状态': '模型更新成功!'})

@app.teardown_request
def check_cache(ctx):
    _cache = get_cache()
    global model
    cached_hash = _cache.get('model_hash')
    if model.hash != cached_hash:
        busy_signal = int(_cache.get('busy_signal'))
        if not busy_signal:
            # 如进程空闲，则将 busi_signal 设置为1，然后更新模型。
            _cache.set('busy_signal', 1)
            model_location = _cache.get('model_location')
            load_model(model_location,_cache)
            _cache.set('busy_signal', 0)
def get_cache():
    if 'cache' not in g:
        g.cache = redis.Redis(decode_responses='utf-8')
    return g.cache
