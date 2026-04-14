FROM maven:3.9-eclipse-temurin-21
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "target/diabetes-backend-1.0.0.jar"]