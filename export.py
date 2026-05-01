#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import sys

SUPPORTED = {
    "1": {"label": "Paper 1.20.6", "paper": "1.20.6-R0.1-SNAPSHOT", "java": "21"},
    "2": {"label": "Paper 1.21.1", "paper": "1.21.1-R0.1-SNAPSHOT", "java": "21"},
}


def update_build_file(path: Path, paper: str) -> None:
    content = path.read_text(encoding="utf-8")
    lines = []
    for line in content.splitlines():
        if 'compileOnly("io.papermc.paper:paper-api:' in line:
            lines.append(f'    compileOnly("io.papermc.paper:paper-api:{paper}")')
        else:
            lines.append(line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_gradle_command(project_dir: Path) -> list[str]:
    if sys.platform.startswith("win"):
        wrapper = project_dir / "gradlew.bat"
        if wrapper.exists():
            return ["cmd", "/c", str(wrapper)]

        repo_wrapper = Path(__file__).resolve().parent / "gradlew.bat"
        if repo_wrapper.exists():
            return ["cmd", "/c", str(repo_wrapper)]

        gradle_bat = shutil.which("gradle.bat") or shutil.which("gradle")
        if gradle_bat:
            return ["cmd", "/c", gradle_bat]

        raise FileNotFoundError("gradlew.bat 또는 gradle(.bat) 명령을 찾을 수 없습니다.")

    wrapper = project_dir / "gradlew"
    if wrapper.exists():
        return [str(wrapper)]

    repo_wrapper = Path(__file__).resolve().parent / "gradlew"
    if repo_wrapper.exists():
        return [str(repo_wrapper)]

    gradle_bin = shutil.which("gradle")
    if gradle_bin:
        return [gradle_bin]

    raise FileNotFoundError("gradlew 또는 gradle 명령을 찾을 수 없습니다.")


def main() -> None:
    base = Path(__file__).resolve().parent

    project_name = input("추출할 플러그인 폴더명을 입력하세요 (예: runningtest): ").strip()
    if not project_name:
        print("폴더명을 입력해야 합니다.")
        raise SystemExit(1)

    project_dir = base / project_name
    build_file = project_dir / "build.gradle.kts"

    if not project_dir.exists() or not build_file.exists():
        print(f"유효한 플러그인 폴더가 아닙니다: {project_dir}")
        raise SystemExit(1)

    print("빌드할 Paper 버전을 선택하세요:")
    for key, value in SUPPORTED.items():
        print(f"  {key}) {value['label']} (paper-api {value['paper']}, Java {value['java']})")

    choice = input("선택 번호 입력: ").strip()
    if choice not in SUPPORTED:
        print("지원하지 않는 선택입니다.")
        raise SystemExit(1)

    selected = SUPPORTED[choice]
    update_build_file(build_file, selected["paper"])
    print(f"선택 완료: {selected['label']}")
    print(f"{project_name} 플러그인 빌드를 시작합니다...")

    try:
        gradle_cmd = resolve_gradle_command(project_dir)
    except FileNotFoundError as error:
        print(f"빌드 도구를 찾지 못했습니다: {error}")
        raise SystemExit(1)

    if (project_dir / "gradlew").exists() or (project_dir / "gradlew.bat").exists():
        run_cmd = [*gradle_cmd, "clean", "build"]
        run_cwd = project_dir
    else:
        run_cmd = [*gradle_cmd, "-p", str(project_dir), "clean", "build"]
        run_cwd = base

    result = subprocess.run(run_cmd, cwd=run_cwd)
    if result.returncode != 0:
        print("빌드 실패: JDK 버전 또는 네트워크 환경을 확인하세요.")
        raise SystemExit(result.returncode)

    jars = sorted((project_dir / "build" / "libs").glob("*.jar"))
    if not jars:
        print("빌드는 성공했지만 JAR 파일을 찾지 못했습니다.")
        raise SystemExit(1)

    print(f"완료: 생성된 파일 -> {jars[-1]}")


if __name__ == "__main__":
    main()
