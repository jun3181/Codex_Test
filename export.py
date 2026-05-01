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
    updated = content.replace(
        'compileOnly("io.papermc.paper:paper-api:1.20.6-R0.1-SNAPSHOT")',
        f'compileOnly("io.papermc.paper:paper-api:{paper}")'
    ).replace(
        'compileOnly("io.papermc.paper:paper-api:1.21.1-R0.1-SNAPSHOT")',
        f'compileOnly("io.papermc.paper:paper-api:{paper}")'
    )
    path.write_text(updated, encoding="utf-8")


def resolve_gradle_command(base: Path) -> list[str]:
    if sys.platform.startswith("win"):
        wrapper = base / "gradlew.bat"
        if wrapper.exists():
            return ["cmd", "/c", str(wrapper)]

        gradle_bat = shutil.which("gradle.bat") or shutil.which("gradle")
        if gradle_bat:
            return ["cmd", "/c", gradle_bat]

        raise FileNotFoundError("gradlew.bat 또는 gradle(.bat) 명령을 찾을 수 없습니다.")

    wrapper = base / "gradlew"
    if wrapper.exists():
        return [str(wrapper)]

    gradle_bin = shutil.which("gradle")
    if gradle_bin:
        return [gradle_bin]

    raise FileNotFoundError("gradlew 또는 gradle 명령을 찾을 수 없습니다.")


def main() -> None:
    base = Path(__file__).resolve().parent
    build_file = base / "build.gradle.kts"

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
    print("Gradle로 JAR 빌드를 시작합니다...")

    try:
        gradle_cmd = resolve_gradle_command(base)
    except FileNotFoundError as error:
        print(f"빌드 도구를 찾지 못했습니다: {error}")
        print("해결 방법: Gradle 설치 후 PATH 등록, 또는 프로젝트에 Gradle Wrapper(gradlew/gradlew.bat) 추가")
        raise SystemExit(1)

    result = subprocess.run([*gradle_cmd, "clean", "build"], cwd=base)
    if result.returncode != 0:
        print("빌드 실패: JDK 버전 또는 네트워크 환경을 확인하세요.")
        raise SystemExit(result.returncode)

    jars = sorted((base / "build" / "libs").glob("*.jar"))
    if not jars:
        print("빌드는 성공했지만 JAR 파일을 찾지 못했습니다.")
        raise SystemExit(1)

    print(f"완료: 생성된 파일 -> {jars[-1]}")
    print("이 JAR 파일을 Minecraft Paper 서버의 plugins 폴더에 넣고 서버를 재시작하세요.")


if __name__ == "__main__":
    main()
