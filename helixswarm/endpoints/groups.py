from typing import Dict, List, Optional, Union

from helixswarm.exceptions import SwarmError
from helixswarm.helpers import minimal_version


class Groups:

    def __init__(self, swarm) -> None:
        self.swarm = swarm

    @minimal_version(2)
    def get(self,
            *,
            after: Optional[str] = None,
            limit: Optional[int] = None,
            fields: Optional[List[str]] = None,
            keywords: Optional[str] = None
            ) -> dict:
        """
        Get the complete list of groups.

        Args:
            after (Optional[str]):
                A group ID to seek to. Groups prior to and including the specified
                ID are excluded from the results and do not count towards `limit`.
                Useful for pagination. Commonly set to the `lastSeen` property from
                a previous query.

            limit (Optional[int]):
                Maximum number of groups to return. This does not guarantee that
                `limit` groups are returned. It does guarantee that the number of
                groups returned won't exceed `limit`.

                Default: 100.

            fields (Optional[List[str]]):
                List of fields to show for each group. Omitting this parameter
                or passing an empty value shows all fields.

            keywords (Optional[str]):
                Keywords to limit groups on. Only groups where the group ID,
                group name (if set), or description contain the specified keywords
                are returned.

        Returns:
            dict: json response.
        """
        params = dict()  # type: Dict[str, Union[str, int]]

        if after:
            params['after'] = after

        if limit:
            params['max'] = limit

        if fields:
            params['fields'] = ','.join(fields)

        if keywords:
            params['keywords'] = keywords

        return self.swarm._request('GET', 'groups', params=params)

    @minimal_version(2)
    def get_info(self,
                 identifier: str,
                 *,
                 fields: Optional[List[str]]
                 ) -> dict:
        """
        Retrieve information about a group.

        Args:
            identifier (str):
                Group identifier.

            fields (Optional[List[str]]):
                List of fields to show for each group. Omitting this parameter
                or passing an empty value shows all fields.

        Returns:
            dict: json response.
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'groups/{}'.format(identifier),
            params=params
        )

        return response

    @minimal_version(2)
    def create(self,
               identifier: str,
               *,
               users: Optional[List[str]] = None,
               owners: Optional[List[str]] = None,
               subgroups: Optional[List[str]] = None,
               name: Optional[str] = None,
               description: Optional[str] = None,
               email_address: Optional[str] = None,
               notify_reviews: Optional[bool] = None,
               notify_commits: Optional[bool] = None,
               use_mailing_list: Optional[bool] = None,
               max_results: Optional[int] = None,
               max_scan_rows: Optional[int] = None,
               max_lock_time: Optional[int] = None,
               max_open_files: Optional[int] = None,
               max_memory: Optional[int] = None,
               timeout: Optional[int] = None,
               password_timeout: Optional[int] = None
               ) -> dict:
        """
        Create a new group.

        Args:
            identifier (str):
                Group identifier.

            users (Optional[List[str]):
                An optional array of group users.
                **At least one of Users, Owners, or Subgroups is required.**

            owners (Optional[List[str]]):
                An optional array of group owners.
                **At least one of Users, Owners, or Subgroups is required.**

            subgroups (Optional[List[str]):
                An optional array of group subgroups.
                **At least one of Users, Owners, or Subgroups is required.**

            name (Optional[str]):
                An optional full name for the group.

            description (Optional[str]):
                An optional group description.

            email_address (Optional[str]):
                The email address for this group.

            notify_reviews (Optional[bool]):
                Email members when a new review is requested.

            notify_commits (Optional[bool]):
                Email members when a change is committed.

            use_mailing_list (Optional[bool]):
                Whether to use the configured email address or expand individual
                members addresses.

            max_results: Optional[int]:

            max_scan_rows: Optional[int]:

            max_lock_time: Optional[int]:

            max_open_files: Optional[int]:

            max_memory: Optional[int]:

            timeout: Optional[int]:

            password_timeout: Optional[int]:

        Returns:
            dict: json response.
        """
        data = dict()  # type: Dict[str, Union[str, bool, List[str]]]

        data['Group'] = identifier

        if not (users or owners or subgroups):
            raise SwarmError('At least one of users, owners, or subgroups is required')

        if users:
            data['Users'] = users

        if owners:
            data['Owners'] = owners

        if subgroups:
            data['Subgroups'] = subgroups

        if name:
            data['config[name]'] = name

        if description:
            data['config[description]'] = description

        if email_address:
            data['config[emailAddress]'] = email_address

        if notify_reviews:
            data['config[emailFlags][reviews]'] = notify_reviews

        if notify_commits:
            data['config[emailFlags][commits]'] = notify_commits

        if use_mailing_list:
            data['config[useMailingList]'] = use_mailing_list

        if max_results:
            data['MaxResults'] = max_results

        if max_scan_rows:
            data['MaxScanRows'] = max_scan_rows

        if max_lock_time:
            data['MaxLockTime'] = max_lock_time

        if max_open_files:
            data['MaxOpenFiles'] = max_open_files

        if max_memory:
            data['MaxMemory'] = max_memory

        if timeout:
            data['Timeout'] = timeout

        if password_timeout:
            data['PasswordTimeout'] = password_timeout

        version = self.swarm.get_version()
        if 11 in version['apiVersions']:
            return self.swarm._request('POST', 'groups', json=data)

        return self.swarm._request('POST', 'groups', data=data)

    @minimal_version(2)
    def edit(self,
             identifier: str,
             *,
             users: Optional[List[str]] = None,
             owners: Optional[List[str]] = None,
             subgroups: Optional[List[str]] = None,
             name: Optional[str] = None,
             description: Optional[str] = None,
             email_address: Optional[str] = None,
             notify_reviews: Optional[bool] = None,
             notify_commits: Optional[bool] = None,
             use_mailing_list: Optional[bool] = None
             ) -> dict:
        """
        Change the settings of a group, only super users and group owners can
        perform this action.

        Args:
            identifier (str):
                Group identifier.

            users (Optional[List[str]):
                An optional array of group users.
                **At least one of Users, Owners, or Subgroups is required.**

            owners (Optional[List[str]):
                An optional array of group owners.
                **At least one of Users, Owners, or Subgroups is required.**

            subgroups (Optional[List[str]):
                An optional array of group subgroups.
                **At least one of Users, Owners, or Subgroups is required.**

            name (Optional[str]):
                An optional full name for the group.

            description (Optional[str]):
                An optional group description.

            email_address (Optional[str]):
                The email address for this group.

            notify_reviews (Optional[bool]):
                Email members when a new review is requested.

            notify_commits (Optional[bool]):
                Email members when a change is committed.

            use_mailing_list (Optional[bool]):
                Whether to use the configured email address or expand individual
                members addresses.

        Returns:
            dict: json response.
        """
        data = dict()  # type: Dict[str, Union[str, bool, List[str]]]

        if users:
            data['Users'] = users

        if owners:
            data['Owners'] = owners

        if subgroups:
            data['Subgroups'] = subgroups

        if name:
            data['config[name]'] = name

        if description:
            data['config[description]'] = description

        if email_address:
            data['config[emailAddress]'] = email_address

        if notify_reviews:
            data['config[emailFlags][reviews]'] = notify_reviews

        if notify_commits:
            data['config[emailFlags][commits]'] = notify_commits

        if use_mailing_list:
            data['config[useMailingList]'] = use_mailing_list

        response = self.swarm._request(
            'PATCH',
            'groups/{}'.format(identifier),
            data=data
        )

        return response

    @minimal_version(2)
    def delete(self, identifier: str) -> dict:
        """
        Delete a group, only super users and group owners can perform this action.

        Args:
            identifier (str):
                Group identifier.

        Returns:
            dict: json response.
        """
        return self.swarm._request('DELETE', 'groups/{}'.format(identifier))
