#!/usr/bin/env python
"""
Define class User
"""

from api.v1.models.BaseModel import BaseModel
from api.v1.models.repo import Repo
from api.v1.app import github


# import requests as github


# import asyncio

class User(BaseModel):
    g_login = ""
    g_home = "http://github.com"
    __repos = {}
    __lang_metric = {}
    __is_login = False

    def __init__(self, user=None):
        """
        This instantiates an new object, if a user and not provided the logged
        in user is used.
        :param user: optional param for check another users metrics on github
        """
        if user:
            me = github.get("/users/{}".format(user)).json()
        else:
            me = github.get("/user").json()
            self.__is_login = True
        data = dict(
            id=me['id'],
            g_login=me["login"],
            g_url=me["url"],
            repos={},
        )
        super().__init__(**data)

    def get_repos(self):
        """
        This Method gets the user's repos processes and convert them to Objects
        :return: dictionary of Repo objects
        """
        temp_d = {}
        if self.is_login:
            resp = github.get("/user/repos").json()
        else:
            resp = github.get("/users/{}/repos".format(self.g_login)).json()
            # print(resp)
        for repo in resp:
            data = dict(
                id=repo["id"],
                owner=self.g_login,
                name=repo["name"],
                url=repo["html_url"],
                __lang={},
                is_owner=(
                    True if repo["owner"]["login"] == self.g_login else False
                ),
                is_fork=repo["fork"]
            )
            new_repo = Repo(**data)
            temp_d.update({"{}".format(data['id']): new_repo.to_dict()})
        self.__repos = temp_d

    def sum_lang(self):
        """
        This method looks at the 'lang' attribute of all the Repos and sums the
        key value pairs.

        :return: Sum of all the key value.
        """
        temp_d = {}
        for repo in self.__repos.values():
            # print(repo)
            for k, v in repo["__lang"].items():
                if k in self.__lang_metric.keys():
                    temp_d[k] += v
                else:
                    temp_d[k] = v
        print(temp_d)
        self.__lang_metric = temp_d




    @property
    def repo(self):
        return self.__repos

    @property
    def lang_metric(self):
        if not self.__lang_metric:
            if not self.__repos:
                self.get_repos()
            self.sum_lang()

        return self.__lang_metric

    @property
    def is_login(self):
        return self.__is_login

    # def async_get_repos(self):
    #     """
    #     Async Method gets the user's repos processes and convert them to Objects
    #     :return: dictionary of Repo objects
    #     """
    #     if self.is_login:
    #         resp = github.get(f"/user/repos").json()
    #     else:
    #         resp = github.get(f"/users/{self.g_login}/repos").json()
    #         print(resp[0])
    #
    #     asyncio \
    #         .get_event_loop() \
    #         .run_until_complete(self.__async__get__repo(resp))
    #
    # async def __async__get__repo(self, resp=None):
    #     await asyncio.sleep(0)
    #     async for repo in resp:
    #         data = dict(
    #             id=repo["id"],
    #             owner=self.g_login,
    #             name=repo["name"],
    #             url=repo['html_url'],
    #             __lang={},
    #             is_owner=(
    #                 True if repo['owner']['login'] == self.g_login else False
    #             ),
    #             is_fork=repo['fork']
    #         )
    #         new_repo = Repo(**data).async_get_lang()
    #         self.__repos.update({f"data['id']": new_repo})
