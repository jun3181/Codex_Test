plugins {
    java
}

group = "com.example"
version = "0.1.0"

repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
}

dependencies {
    compileOnly("io.papermc.paper:paper-api:${project.findProperty("paperVersion") ?: "1.20.6-R0.1-SNAPSHOT"}")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of((project.findProperty("javaVersion") ?: "21").toString().toInt()))
    }
}

tasks.withType<JavaCompile>().configureEach {
    options.encoding = "UTF-8"
}

tasks.processResources {
    filteringCharset = "UTF-8"
}
