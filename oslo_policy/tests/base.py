# Copyright (c) 2015 OpenStack Foundation.
# All Rights Reserved.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os.path

from oslo_config import fixture as config
from oslotest import base as test_base

from oslo_policy import _checks
from oslo_policy import policy


TEST_VAR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', 'tests/var'))


class PolicyBaseTestCase(test_base.BaseTestCase):

    def setUp(self):
        super(PolicyBaseTestCase, self).setUp()
        self.conf = self.useFixture(config.Config()).conf
        self.conf(args=['--config-dir', TEST_VAR_DIR])
        self.enforcer = policy.Enforcer(self.conf)
        self.addCleanup(self.enforcer.clear)


class FakeCheck(_checks.BaseCheck):
    def __init__(self, result=None):
        self.result = result

    def __str__(self):
        return str(self.result)

    def __call__(self, target, creds, enforcer):
        if self.result is not None:
            return self.result
        return (target, creds, enforcer)
