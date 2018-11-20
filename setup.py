from setuptools import setup
setup(name='ampel-base',
      version='0.5.1',
      package_dir={'':'src'},
      packages=[
          'ampel.base',
          'ampel.base.abstract',
          'ampel.base.dev',
          'ampel.base.flags',
          'ampel.utils',
      ]
)
