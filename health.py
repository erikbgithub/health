import flask
import os
import json
import subprocess

app = flask.Flask(__name__)

def docker_stats():
  return [json.loads(l if l else "{}") for l in subprocess.Popen('docker stats --no-stream --format \'{"container" : "{{ .Container }}","memory":{"usage": "{{ .MemUsage }}", "percent":"{{ .MemPerc }}"}, "cpu": "{{ .CPUPerc }}"}\'', shell=True, stdout=subprocess.PIPE).stdout.read().split('\n') if l]

def cpu_stats():
  return { 'cpu' + str(c) : subprocess.Popen("grep 'cpu{} ' /proc/stat|awk '{{usage=($2+$4)*100/($2+$4+$5)}} END {{printf \"%2.2f%%\", usage}}'".format(str(c)), shell=True, stdout=subprocess.PIPE).stdout.read() for c in ['',0,1,2,3] }

@app.route('/healthz')
def healthz():
  status = statusz()
  cpu_str=json.loads(status).get('host',{}).get('cpu','-0.0%')
  cpu_load=float(cpu_str[:-1])
  if cpu_load > 95.0:
    flask.abort(500, "cpu load too high ({})".format(cpu_str))
  else:
    return "ok"

@app.route('/statusz')
def statusz():
  return json.dumps({
    'statuspid' : str(os.getpid()),
    'docker' : docker_stats(),
    'host' : cpu_stats(),
  },indent=2)
