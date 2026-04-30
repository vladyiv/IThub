{\rtf1\ansi\ansicpg1251\cocoartf2580
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red88\green148\blue206;\red255\green255\blue255;\red202\green202\blue202;
\red212\green212\blue212;\red167\green197\blue151;\red212\green213\blue154;\red188\green135\blue185;\red141\green212\blue254;
\red194\green126\blue101;\red67\green192\blue160;}
{\*\expandedcolortbl;;\cssrgb\c41371\c64935\c84491;\cssrgb\c100000\c100000\c100000\c0;\cssrgb\c83229\c83229\c83125;
\cssrgb\c86370\c86370\c86262;\cssrgb\c71008\c80807\c65805;\cssrgb\c86261\c86245\c66529;\cssrgb\c78876\c61228\c77620;\cssrgb\c61361\c86489\c99746;
\cssrgb\c80778\c56830\c46925;\cssrgb\c30610\c78876\c69022;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sl380\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 class\cf4 \strokec4  User\cf5 \strokec5 :\cf4 \strokec4 \
\
  __count = \cf6 \strokec6 0\cf4 \strokec4 \
\
  \cf7 \strokec7 @staticmethod\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 get_count\cf4 \strokec4 ()\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  User.__count\
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 __init__\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 name\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 login\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 password\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 grade\cf4 \strokec4 : \cf9 \strokec9 int\cf4 \strokec4  = \cf6 \strokec6 1\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4 \
    \cf8 \strokec8 if\cf4 \strokec4  grade <= \cf6 \strokec6 0\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 print\cf5 \strokec5 (\cf10 \strokec10 '
\f1 \cf10 \strokec10 \uc0\u1047 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1077 
\f0 \cf10 \strokec10  grade 
\f1 \cf10 \strokec10 \uc0\u1076 \u1086 \u1083 \u1078 \u1085 \u1086 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1073 \u1099 \u1090 \u1100 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1087 \u1086 \u1083 \u1086 \u1078 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1099 \u1084 
\f0 \cf10 \strokec10 ! 
\f1 \cf10 \strokec10 \uc0\u1055 \u1088 \u1080 \u1089 \u1074 \u1086 \u1077 \u1085 \u1086 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1077 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1087 \u1086 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102 
\f0 \cf10 \strokec10 .'\cf5 \strokec5 )\cf4 \strokec4 \
    \cf9 \strokec9 self\cf4 \strokec4 .name = name\
    \cf9 \strokec9 self\cf4 \strokec4 .__login = login\
    \cf9 \strokec9 self\cf4 \strokec4 .password = password\
    \cf9 \strokec9 self\cf4 \strokec4 .grade = grade\
    User.__count += \cf6 \strokec6 1\cf4 \strokec4 \
  \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 show_info\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4 \
    role_name = \cf10 \strokec10 ''\cf4 \strokec4 \
    \cf8 \strokec8 if\cf4 \strokec4  \cf11 \strokec11 type\cf5 \strokec5 (\cf9 \strokec9 self\cf5 \strokec5 )\cf4 \strokec4  == SuperUser\cf5 \strokec5 :\cf4 \strokec4  role_name = \cf2 \strokec2 f\cf10 \strokec10 ', Role: \cf5 \strokec5 \{\cf9 \strokec9 self\cf4 \strokec4 .role\cf5 \strokec5 \}\cf10 \strokec10 '\cf4 \strokec4  \
    \cf7 \strokec7 print\cf5 \strokec5 (\cf2 \strokec2 f\cf10 \strokec10 'Name: \cf5 \strokec5 \{\cf9 \strokec9 self\cf4 \strokec4 .name\cf5 \strokec5 \}\cf10 \strokec10 , login: \cf5 \strokec5 \{\cf9 \strokec9 self\cf4 \strokec4 .__login\cf5 \strokec5 \}\cf10 \strokec10 '\cf4 \strokec4  + role_name\cf5 \strokec5 )\cf4 \strokec4 \
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 __lt__\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 user\cf4 \strokec4 : '\cf9 \strokec9 User\cf4 \strokec4 ')\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf9 \strokec9 self\cf4 \strokec4 .grade < user.grade\
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 __gt__\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 user\cf4 \strokec4 : '\cf9 \strokec9 User\cf4 \strokec4 ')\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf9 \strokec9 self\cf4 \strokec4 .grade > user.grade\
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 __eq__\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 user\cf4 \strokec4 : '\cf9 \strokec9 User\cf4 \strokec4 ')\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf9 \strokec9 self\cf4 \strokec4 .grade == user.grade\
\
  \cf7 \strokec7 @property\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 grade\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf10 \strokec10 '
\f1 \cf10 \strokec10 \uc0\u1053 \u1077 \u1080 \u1079 \u1074 \u1077 \u1089 \u1090 \u1085 \u1086 \u1077 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1089 \u1074 \u1086 \u1081 \u1089 \u1090 \u1074 \u1086 
\f0 \cf10 \strokec10  grade'\cf4 \strokec4 \
  \cf7 \strokec7 @grade.setter\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 grade\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 value\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 print\cf5 \strokec5 (\cf10 \strokec10 '
\f1 \cf10 \strokec10 \uc0\u1053 \u1077 \u1080 \u1079 \u1074 \u1077 \u1089 \u1090 \u1085 \u1086 \u1077 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1089 \u1074 \u1086 \u1081 \u1089 \u1090 \u1074 \u1086 
\f0 \cf10 \strokec10  grade'\cf5 \strokec5 )\cf4 \strokec4 \
\
  \cf7 \strokec7 @property\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 password\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf10 \strokec10 '*'\cf4 \strokec4  * \cf7 \strokec7 len\cf5 \strokec5 (\cf9 \strokec9 self\cf4 \strokec4 .__password\cf5 \strokec5 )\cf4 \strokec4 \
  \cf7 \strokec7 @password.setter\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 password\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 value\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4         \
      \cf9 \strokec9 self\cf4 \strokec4 .__password = value\
\
  \cf7 \strokec7 @property\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 login\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  \cf9 \strokec9 self\cf4 \strokec4 .__login\
  \cf7 \strokec7 @login.setter\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 login\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 value\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4  \cf7 \strokec7 print\cf5 \strokec5 (\cf10 \strokec10 '
\f1 \cf10 \strokec10 \uc0\u1053 \u1077 \u1074 \u1086 \u1079 \u1084 \u1086 \u1078 \u1085 \u1086 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1080 \u1079 \u1084 \u1077 \u1085 \u1080 \u1090 \u1100 
\f0 \cf10 \strokec10  
\f1 \cf10 \strokec10 \uc0\u1083 \u1086 \u1075 \u1080 \u1085 
\f0 \cf10 \strokec10 !'\cf5 \strokec5 )\cf4 \strokec4 \
\
\pard\pardeftab720\sl380\partightenfactor0
\cf2 \strokec2 class\cf4 \strokec4  \cf11 \strokec11 SuperUser\cf4 \strokec4 (\cf11 \strokec11 User\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4 \
\
  __count = \cf6 \strokec6 0\cf4 \strokec4 \
\
  \cf7 \strokec7 @staticmethod\cf4 \strokec4 \
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 get_count\cf4 \strokec4 ()\cf5 \strokec5 :\cf4 \strokec4  \cf8 \strokec8 return\cf4 \strokec4  SuperUser.__count\
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 __init__\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 , \cf9 \strokec9 name\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 login\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 password\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 role\cf4 \strokec4 : \cf9 \strokec9 str\cf4 \strokec4 , \cf9 \strokec9 grade\cf4 \strokec4 : \cf9 \strokec9 int\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4 \
    super\cf5 \strokec5 ()\cf4 \strokec4 .\cf7 \strokec7 __init__\cf5 \strokec5 (\cf4 \strokec4 name\cf5 \strokec5 ,\cf4 \strokec4  login\cf5 \strokec5 ,\cf4 \strokec4  password\cf5 \strokec5 ,\cf4 \strokec4  grade\cf5 \strokec5 )\cf4 \strokec4 \
    \cf9 \strokec9 self\cf4 \strokec4 .role = role\
    SuperUser.__count += \cf6 \strokec6 1\cf4 \strokec4 \
\
  \cf2 \strokec2 def\cf4 \strokec4  \cf7 \strokec7 show_info\cf4 \strokec4 (\cf9 \strokec9 self\cf4 \strokec4 )\cf5 \strokec5 :\cf4 \strokec4 \
    super\cf5 \strokec5 ()\cf4 \strokec4 .show_info\cf5 \strokec5 ()\cf4 \strokec4 \
\pard\pardeftab720\sl380\partightenfactor0
\cf4 \strokec4 \
}