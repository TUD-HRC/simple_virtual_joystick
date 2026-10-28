from glob import glob

from setuptools import find_packages, setup

package_name = 'simple_virtual_joystick'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Davide Torielli',
    maintainer_email='toridebraus@gmail.com',
    description='Simple virtual joystick to publish a twist by means of your mouse',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_virtual_joystick = simple_virtual_joystick.simple_virtual_joystick:main',
            'virtual_joystick = simple_virtual_joystick.simple_virtual_joystick:main',
        ],
    },
)
