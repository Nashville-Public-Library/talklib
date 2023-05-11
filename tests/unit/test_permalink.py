import pytest

try:
    from ...show import TLShow
except KeyError:
    pass

url = 'https://pnsne.ws/3mVuTax'

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.is_permalink = True
    # disable notifications for templateing. Need separate templates for these!
    test.notifications = False
    test.syslog_enable = False

    return test

# ---------- check attributes ----------

def test_attrib_1a(template: TLShow):
    template.show = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1b(template: TLShow):
    template.show = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1c(template: TLShow):
    template.show = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1d(template: TLShow):
    template.show = ''
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2a(template: TLShow):
    template.show_filename = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2b(template: TLShow):
    template.show_filename = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2c(template: TLShow):
    template.show_filename = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2d(template: TLShow):
    template.show_filename = ''
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_3a(template: TLShow):
    template.url = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_3b(template: TLShow):
    template.url = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_4b(template: TLShow):
    template.is_permalink = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_4c(template: TLShow):
    template.is_permalink = 'not boolean'
    with pytest.raises(Exception):
        template.check_attributes_are_valid()