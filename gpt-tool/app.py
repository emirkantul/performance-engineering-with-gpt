from flask import Flask, render_template, request
from prompter import (
    get_performance_issues,
    get_architecture_recommendation,
    get_perf_assessment,
    get_nvprof_assessment,
    get_fix,
)
from ssh import SSHConnection
import time

app = Flask(__name__)

last_resp = None
ssh = SSHConnection()
ssh.connect()


@app.route("/fix", methods=["GET"])
def fix():
    start = time.time()
    global last_resp
    perf_results = None
    nvprof_results = None
    fixed_results = get_fix(last_resp)
    if last_resp.get("runnable", None) is not None:
        if last_resp.get("is_cuda", None) is not None:
            nvprof_results = ssh.exec_cuda_code(
                input_code=fixed_results["new_code"],
                additional_options=last_resp["additional_options"],
            )
        perf_results = ssh.exec_cpp_code(
            input_code=fixed_results["new_code"],
            additional_options=last_resp["additional_options"],
        )

    end = time.time()
    print(f"Time taken: {end - start}")
    return render_template(
        "fix.html",
        resp={
            "previous_code": last_resp.get("code"),
            "new_code": fixed_results["new_code"],
            "previous_nvprof_results": last_resp["nvprof_results"],
            "new_nvprof_results": nvprof_results["nvprof"]
            if nvprof_results is not None
            else None,
            "previous_perf_results": last_resp["perf_results"],
            "new_perf_results": perf_results["perf"]
            if perf_results is not None
            else None,
            "whats_changed": fixed_results["whats_changed"],
        },
    )


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        start = time.time()
        global last_resp
        code = request.form.get("code")
        cpu = request.form.get("cpu", None)
        gpu = request.form.get("gpu", None)
        runnable = request.form.get("runnable", None)
        additional_options = request.form.get("additional_options", "")
        is_cuda = request.form.get("is_cuda", None)
        perf_results = None
        nvprof_results = None
        architecture_recommendations = None

        performance_issues = get_performance_issues(code)

        if cpu is not None or gpu is not None:
            architecture_recommendations = get_architecture_recommendation(
                code, cpu, gpu
            )

        if runnable is not None:
            if is_cuda is not None:
                nvprof_results = ssh.exec_cuda_code(
                    input_code=code, additional_options=additional_options
                )
                nvprof_assessment = get_nvprof_assessment(code, nvprof_results)
            perf_results = ssh.exec_cpp_code(
                input_code=code, additional_options=additional_options
            )
            if perf_results is not None:
                perf_assessment = get_perf_assessment(code, perf_results)

        resp = {
            "performance_issues": performance_issues,
            "architecture_recommendations": architecture_recommendations,
            "perf_results": perf_results["perf"] if perf_results else None,
            "perf_assessment": perf_assessment if perf_results else None,
            "nvprof_results": nvprof_results["nvprof"]
            if nvprof_results
            else None,
            "nvprof_assessment": nvprof_assessment if nvprof_results else None,
            "code": code,
            "runnable": runnable,
            "is_cuda": is_cuda,
            "additional_options": additional_options,
            "gpu": gpu,
            "cpu": cpu,
        }
        last_resp = resp
        end = time.time()
        print(f"Time taken: {end - start}")
        return render_template(
            "index.html",
            resp=resp,
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
