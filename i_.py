# 변수 = 값
#       숫자

#주석 = Cntrl + /



a = 5

print(a)

a = 5
a = 3
print(a)

c = 10
d = 5
print( c + d )
print( c - d )
print( c * d )
print( c / d )
print( c // d )
print( c % d )

name = 이연진
print(name)

name = '이연진'
print(name)

name = "이연진"
print(name)

c1 = "데이터"
c2 = '분석'
print(c1+c2)
print(c2+c1)

print('-------------------------')
print('-'*20)



# 분석 = 값
#     숫자, 문자, 그룹,,

# 변수는 띄어쓰기 안됨 _나 / 사용

# 명령어( )
# [ ]
#  -  리스트 : [원소1, 원소2, ,]
#  -  선택할때 : 그룹[key]
# : 범위 > [a:b] = a 이상 b 미만

song_list = [ '도깨비불', 'zombie', 'stay this way', 'vacation', 'ring the alarm' ]
song = '도깨비불'
song = song_list[2]
song=song_list[-1]
song = song_list[0:2][1]
print(song_list)
print(song)



# 반복문

song_list = [ '도깨비불', 'zombie', 'stay this way', 'vacation', 'ring the alarm' ]
for song in song_list:
    print(song)

msg = '안녕하세요 홍길동님. 가입해주셔서 감사합니다. '
print(msg)



#f-string

name_list = ['홍길동', '철수', '영희' ]
for name in name_list:
    msg = f'안녕하세요 {name} 님. 가입해주셔서 감사합니다. '
    print(msg)



