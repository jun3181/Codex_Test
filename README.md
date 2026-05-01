# Minecraft Plugin Starter

마인크래프트(Paper) 플러그인 개발을 바로 시작할 수 있도록 기본 환경을 구성했습니다.

## 요구 사항
- JDK 21
- Gradle 8+

## 빌드
```bash
./gradlew build
```

## 적용 방법
1. 빌드 후 `build/libs/*.jar` 파일을 Paper 서버의 `plugins/` 폴더에 넣습니다.
2. 서버를 재시작하면 `StarterPlugin`이 로드됩니다.

## 다음 단계 추천
- 명령어 등록 (`plugin.yml` + CommandExecutor)
- 이벤트 리스너 추가 (`Listener` + `@EventHandler`)
- 설정 파일(`config.yml`) 로드
