# moveit_core.launch.py
# /home/moonshot/Manipulator_only/src/manipulator_moveit/launch/moveit_core.launch.py

# manipulator_perception.launch.py
# 눌러야하는 버튼 넣어줘야할듯.
# /home/moonshot/Manipulator_only/src/camera_perception_pkg/launch/manipulator_perception.launch.py

# marker_moveit_commander.py
# /home/moonshot/Manipulator_only/src/manipulator_manager/manipulator_manager/marker_moveit_commander.py

자 이런식으로 우리가 코드를 정리해서 최종적으로 manipulator_all_in_one.launch를 만들거야.
그런데 다만 생각해야하는 부분들이 먼저 있어서 이부분들을 바로잡고 런치를 묶는 과정으로 가고자 해.

1. moveit_core.launch.py 이 부분은 이미 완전히 완성되어있어서 건들 필요가 없음.

2. manipulator_perception.launch.py 이 부분은 일단 인식하고자 하는 버튼을 넘겨줘야하는 구조라서 이 버튼 누르는 것에 대한 관리가 필요함.

3. marker_moveit_commander.py 이 부분의 경우 config 안에 로봇 팔동작에 대한 파라미터를 정의하고 바꿔가면서 실험하는 구조가 이상적으로 보여.

어떤 것 부터 시작해볼까?


나는 2번부터 가보는게 좋아보여. 어떤 식으로 구조를 만들면 좋을까? 설정 파일을 하나 추가해야할까? 

moonshot@moonshot:~/Manipulator_only/src/camera_perception_pkg$ tree -L 3
.
├── camera_perception_pkg
│   ├── __init__.py
│   ├── object_distance_node.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── object_distance_node.cpython-310.pyc
│   │   ├── yolov8_debug_node.cpython-310.pyc
│   │   └── yolov8_node.cpython-310.pyc
│   ├── yolov8_debug_node.py
│   └── yolov8_node.py
├── launch
│   └── manipulator_perception.launch.py
├── package.xml
├── resource
│   └── camera_perception_pkg
├── setup.cfg
├── setup.py
└── test
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py