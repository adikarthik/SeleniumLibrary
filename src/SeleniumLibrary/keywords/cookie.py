# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_truthy
from robot.libraries.DateTime import convert_date


class CookieKeywords(LibraryComponent):

    @keyword
    def delete_all_cookies(self):
        """Deletes all cookies."""
        self.browser.delete_all_cookies()

    @keyword
    def delete_cookie(self, name):
        """Deletes cookie matching ``name``.

        If the cookie is not found, nothing happens.
        """
        self.browser.delete_cookie(name)

    @keyword
    def get_cookies(self):
        """Returns all cookies of the current page."""
        pairs = []
        for cookie in self.browser.get_cookies():
            pairs.append(cookie['name'] + "=" + cookie['value'])
        return '; '.join(pairs)

    @keyword
    def get_cookie_value(self, name):
        """Returns value of cookie found with ``name``.

        If no cookie is found with ``name``, this keyword fails.
        """
        cookie = self.browser.get_cookie(name)
        if cookie is not None:
            return cookie['value']
        raise ValueError("Cookie with name %s not found." % name)

    @keyword
    def get_cookie(self, name):
        """Returns a cookie object found with ``name``.

        The cookie object contains details about the cookie.
        Attributes available in the object are documented in the table below.
        | = Attribute = |             = Explanation =                            |
        | domain        | Specifies hosts to which the cookie will be sent       |
        | expiry        | The maximum lifetime of the cookie as EPOCH            |
        | httpOnly      | HttpOnly cookie cannot be accessed by client-side APIs |
        | name          | The name of a cookie                                   |
        | path          | Indicates a URL path, usually /                        |
        | secure        | Cookie will be send only by using secure connection    |
        | value         | Value of the cookie                                    |
        | full_info     | All the above attributes joined as string              |

        If no cookie is found with ``name``, this keyword fails.
        """
        cookie = self.browser.get_cookie(name)
        if cookie:
            return CookieInformation(
                cookie.get('domain', None), cookie.get('expiry', None),
                cookie.get('httpOnly', None), cookie['name'],
                cookie.get('path', None), cookie.get('secure', None),
                cookie['value'])
        raise ValueError("Cookie with name %s not found." % name)

    @keyword
    def add_cookie(self, name, value, path=None, domain=None, secure=None,
                   expiry=None):
        """Adds a cookie to your current session.

        ``name`` and ``value`` are required, ``path``, ``domain``, ``secure``
        and ``expiry`` are optional.  Expiry supports the same formats as
        the DateTime library and is converted to EPOCH which is supported
        by the Selenium.
        """
        new_cookie = {'name': name, 'value': value}
        if is_truthy(path):
            new_cookie['path'] = path
        if is_truthy(domain):
            new_cookie['domain'] = domain
        # Secure should be True or False
        if is_truthy(secure):
            new_cookie['secure'] = secure
        if is_truthy(expiry):
            expiry_datetime = int(convert_date(expiry, result_format='epoch'))
            new_cookie['expiry'] = expiry_datetime
        self.browser.add_cookie(new_cookie)


class CookieInformation(object):
    def __init__(self, domain, expiry, httpOnly, name, path, secure, value):
        self.domain = domain
        self.expiry = expiry
        self.httpOnly = httpOnly
        self.name = name
        self.path = path
        self.secure = secure
        self.value = value

    @property
    def full_info(self):
        return ', '.join("{}={}".format(key, value) for
                         (key, value) in self.__dict__.items())

    def __str__(self):
        return self.full_info
