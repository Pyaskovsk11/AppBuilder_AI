# Dockerfile для автоматизации тестирования (RSpec) и аудита (Brakeman)
FROM ruby:3.2

WORKDIR /app

COPY . /app

RUN gem install bundler && bundle install || true
RUN gem install brakeman

CMD ["irb"]
