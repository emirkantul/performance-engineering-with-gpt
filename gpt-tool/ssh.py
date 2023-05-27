import paramiko
from dotenv import load_dotenv
import os
import time

load_dotenv()

SSH_HOST = os.getenv("SSH_HOST")
SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")
TIMEOUT = 30


class SSHConnection:
    def __init__(self):
        self.ssh = None
        self.attempts = 0
        self.max_attempts = 3
        self.connect()

    def connect(self):
        if self.ssh is None or not self.ssh.get_transport().is_active():
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(
                    SSH_HOST,
                    username=SSH_USER,
                    password=SSH_PASSWORD,
                )
                self.attempts = 0
            except Exception as e:
                print("Error: ", e)
                self.attempts += 1
                if self.attempts <= self.max_attempts:
                    print(
                        "Failed to connect. Retrying"
                        f" ({self.attempts}/{self.max_attempts})..."
                    )
                    self.connect()
                else:
                    print(
                        "Failed to connect after multiple attempts."
                        " Aborting..."
                    )
                    raise

    def exec_cpp_code(self, input_code, additional_options=""):
        remote_path_to_input_code = "~/input_code.cpp"

        # The commands to run
        stdin, stdout, stderr = self.ssh.exec_command(
            f"echo '{input_code}' > {remote_path_to_input_code}"
        )
        exit_status = stdout.channel.recv_exit_status()

        compile_input_code = (  # For C++ codes
            f"g++ -fopenmp {additional_options} {remote_path_to_input_code}"
        )

        run_input_code = "perf record -e cpu-cycles ~/a.out"

        # Compile and run the results
        print("\nCompiling with: " + compile_input_code)
        stdin, stdout, stderr = self.ssh.exec_command(compile_input_code)
        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break
        compile_result = (
            "\nCompile results: "
            + stdout.read().decode("utf-8", errors="replace")
            + stderr.read().decode("utf-8", errors="replace")
            + "\n"
        )
        print(compile_result)
        exit_status = stdout.channel.recv_exit_status()

        print("\nRunning with: " + run_input_code)
        stdin, stdout, stderr = self.ssh.exec_command(run_input_code)

        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break

        exit_status = stdout.channel.recv_exit_status()

        print("\nRunning with: perf report > ~/perf.txt")
        stdin, stdout, stderr = self.ssh.exec_command(
            "perf report > ~/perf.txt"
        )
        stdout.channel.close()

        print("\nRunning with: cat ~/perf.txt")
        stdin, stdout, stderr = self.ssh.exec_command("cat ~/perf.txt")
        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break

        cpu_cycles = (
            "Perf CPU Cycles: "
            + stdout.read().decode("utf-8", errors="replace")
            + stderr.read().decode("utf-8", errors="replace")
            + "\n"
        )
        print(cpu_cycles)
        exit_status = stdout.channel.recv_exit_status()

        print("\nRunning with: perf stat ~/a.out")
        stdin, stdout, stderr = self.ssh.exec_command("perf stat ~/a.out")

        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break

        stats = (
            stdout.read().decode("utf-8", errors="replace")
            + stderr.read().decode("utf-8", errors="replace")
            + "\n"
        )
        stats = stats.split(
            "Performance counter stats for '/home/emirkantul/a.out':"
        )
        run_result = "Run results: " + stats[0]
        stats = "Perf stats: " + stats[-1]
        print(run_result)
        print(stats)
        exit_status = stdout.channel.recv_exit_status()

        return {
            "compile": compile_result,
            "run": run_result,
            "perf": {"cpu_cycles": cpu_cycles, "stats": stats},
        }

    def exec_cuda_code(self, input_code, additional_options=""):
        # Transfer the files to the remote server
        remote_path_to_input_code = "~/input_code.cu"

        # The commands to run
        stdin, stdout, stderr = self.ssh.exec_command(
            f"echo '{input_code}' > {remote_path_to_input_code}"
        )
        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break
        exit_status = stdout.channel.recv_exit_status()

        compile_input_code = (  # For C++ codes
            f"nvcc {remote_path_to_input_code} -Xcompiler -fopenmp"
            f" {additional_options}"
        )
        run_input_code = "nvprof ~/a.out"

        # Compile and run the results
        print("\nCompiling with: " + compile_input_code)
        stdin, stdout, stderr = self.ssh.exec_command(compile_input_code)
        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break
        compile_result = (
            "\nCompile results: "
            + stdout.read().decode("utf-8", errors="replace")
            + stderr.read().decode("utf-8", errors="replace")
            + "\n"
        )
        print(compile_result)
        exit_status = stdout.channel.recv_exit_status()

        print("\nRunning with: " + run_input_code)
        stdin, stdout, stderr = self.ssh.exec_command(run_input_code)
        endtime = time.time() + TIMEOUT
        while not stdout.channel.eof_received:
            time.sleep(1)
            if time.time() > endtime:
                stdout.channel.close()
                print("SSH Timeout")
                break
        run_result = (
            "\nRun results: "
            + stdout.read().decode("utf-8", errors="replace")
            + stderr.read().decode("utf-8", errors="replace")
            + "\n"
        )
        print(run_result)
        exit_status = stdout.channel.recv_exit_status()

        return {
            "compile": compile_result,
            "run": run_result,
            "nvprof": "Nvprof results:"
            + run_result.split("Profiling result:")[-1],
        }

    def close(self):
        if self.ssh is not None and self.ssh.get_transport().is_active():
            self.ssh.close()
