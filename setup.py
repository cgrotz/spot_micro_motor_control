from setuptools import setup

setup(
    name='Spot Micro Motor Control',
    url='https://github.com/cgrotz/spot_micro_motor_control',
    author='Christoph Grotz',
    author_email='christoph.grotz@gmail.com',
    packages=['motor_control'],
    install_requires=['Adafruit_PCA9685'],
    version='0.1',
    license='MIT',
    description='Motor Control Abstraction for Spot Micro',
    long_description=open('README.md').read(),
)
