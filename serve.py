#!/usr/bin/env python3
"""本地静态站预览：启动前打印 IPv4 / IPv6 本机地址（与 README 一致）。"""
import subprocess
import sys

PORT = 8000


def main() -> None:
    p = str(PORT)
    print()
    print("本地预览 — 可在浏览器打开：")
    print(f"  http://127.0.0.1:{p}/")
    print(f"  http://[::]:{p}/   （与下方 Serving HTTP on :: port … 对应）")
    print()
    subprocess.run([sys.executable, "-m", "http.server", p], check=False)


if __name__ == "__main__":
    main()
