> 이 리포지토리는 네트워크 프로그래밍의 기본 개념을 소개하고, Python의 socket 모듈을 활용한 간단한 네트워크 프로그래밍 예제를 제공합니다.

## 개요
이 리포지토리는 Python의 socket 모듈을 활용한 간단한 네트워크 프로그래밍 예제를 제공합니다. 모든 예제는 TCP 및 UDP 소켓을 생성하고, 이를 통해 데이터를 주고받는 방법을 설명합니다.

## 내용
### HW1 : 계산기 만들기
HW1은 클라이언트-서버 기반의 온라인 계산기 애플리케이션을 개발하는 것입니다.  
클라이언트는 사용자로부터 수식을 입력받아 서버로 전송하고, 서버는 수식을 계산하여 결과를 클라이언트에게 반환합니다.  
클라이언트는 반환된 결과를 result.txt 파일에 저장합니다.

### HW2 : 웹서버 만들기
HW2에서는 웹 서버를 만들어 텍스트 파일에 저장된 수식을 읽어 계산한 후, 결과를 Result.html 파일로 저장합니다.  
웹 서버는 한 번에 하나의 HTTP 요청만 처리하며, 클라이언트가 GET 메서드를 통해 Result.html을 요청할 때 다음과 같은 작업을 수행합니다:  
1. 클라이언트로부터 HTTP 요청을 수신하고 분석합니다.  
2. 서버의 파일 시스템에서 요청된 파일을 검색합니다.  
3. 요청된 파일이 존재할 경우, 해당 파일의 내용을 포함한 HTTP 응답 메시지를 생성하여 클라이언트에게 전송합니다.  
4. 요청된 파일이 서버에 존재하지 않을 경우, HTTP "404 Not Found" 메시지를 클라이언트에게 전송합니다.

### HW3: DNS 서버 통신 구현하기
HW3에서는 소켓 프로그래밍을 사용하여 DNS 조회 시스템을 구현합니다.  
이 시스템은 클라이언트와 두 개의 DNS 서버(로컬 DNS 서버, 글로벌 DNS 서버)로 구성됩니다. 클라이언트가 도메인의 IP 주소를 요청할 때 다음 단계가 수행됩니다:  
1. 클라이언트는 domain.txt 파일에서 도메인 이름을 읽어와 로컬 DNS 서버로 전송합니다.
2. 로컬 DNS 서버는 local_dns.txt 파일에서 도메인 이름을 검색합니다. 도메인이 존재하면 해당 IP 주소를 클라이언트에게 반환합니다.
3. 도메인이 로컬 DNS 서버에 없을 경우, 글로벌 DNS 서버로 도메인 이름을 전달하여 IP 주소를 요청합니다. 글로벌 DNS 서버는 global_edu_dns.txt와 global_com_dns.txt 파일에서 도메인 이름을 검색하고, 결과를 로컬 DNS 서버로 반환합니다.
4. 만약 도메인이 글로벌 DNS 서버에도 존재하지 않으면, "Not found" 메시지를 로컬 DNS 서버로 반환합니다.
5. 로컬 DNS 서버는 글로벌 DNS 서버에서 받은 결과를 클라이언트로 전달합니다.
6. 클라이언트는 결과를 result.txt 파일에 기록합니다.

### HW4: 동영상 스트리밍 시스템 만들기
이 과제에서는 소켓 프로그래밍을 사용하여 글로벌 서버, 로컬 서버, 클라이언트를 설정하여 동영상 스트리밍 시스템을 구현합니다.  
세 가지 시나리오가 존재합니다: (동영상은 파일에 포함되어있지 않습니다.)  
시나리오 1:  
클라이언트가 로컬 서버를 통해 글로벌 서버에 Video_2023 동영상을 요청합니다.  
로컬 서버는 이미 해당 동영상을 보유하고 있으므로, 클라이언트에게 직접 동영상을 전송합니다.  
시나리오 2:  
클라이언트가 video_2022 동영상을 요청합니다.  
로컬 서버는 해당 동영상을 보유하고 있지 않아 글로벌 서버에 요청을 전달합니다.  
글로벌 서버는 동영상을 로컬 서버로 전송하며, 로컬 서버는 이를 저장한 후 클라이언트에게 전달합니다.  
시나리오 3:  
클라이언트가 라이브 영상을 요청합니다.  
로컬 서버는 글로벌 서버에 라이브 영상 요청을 전달하며, 글로벌 서버는 영상을 로컬 서버로 스트리밍합니다.  
로컬 서버는 스트리밍된 영상을 클라이언트에게 전달합니다.  

### HW5: 통합 시스템 만들기
HW5는 다수의 클라이언트, 로컬 서버, 글로벌 서버를 포함하는 시나리오에서 동작하는 시스템을 구현하는 것입니다.  
주요 작업은 다음과 같습니다:  
1. 텍스트 애플리케이션 개발: 클라이언트가 계산식을 입력하면 결과를 반환하는 계산기를 개발하여 로컬 및 글로벌 서버에 저장합니다.  
2. 클라이언트, 로컬 서버, 글로벌 서버 구현: 클라이언트와 서버 간의 인증 및 서비스 요청(텍스트, 이미지, 동영상) 처리를 Python 소켓 프로그래밍으로 구현합니다.  
3. 프로세스:  
- 클라이언트는 로컬 서버에 인증을 요청하고, 인증 후 다양한 서비스를 요청합니다.  
- 로컬 서버는 텍스트 계산, 이미지 전송, 그리고 캐시된 동영상(video_2023)을 제공합니다.  
- video_2022 요청 시, 로컬 서버는 글로벌 서버에서 영상을 받아 클라이언트에 전송합니다.  
