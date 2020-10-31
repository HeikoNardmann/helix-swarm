from typing import Dict, List, Optional, Union

from helixswarm.exceptions import SwarmCompatibleError


class Reviews:

    def __init__(self, swarm):
        self.swarm = swarm

    def get(self,
            *,
            after: Optional[int] = None,
            limit: Optional[int] = None,
            fields: Optional[List[str]] = None,
            authors: Optional[List[str]] = None,
            changes: Optional[List[int]] = None,
            has_reviewers: Optional[bool] = None,
            ids: Optional[List[int]] = None,
            keywords: Optional[str] = None,
            participants: Optional[List[str]] = None,
            projects: Optional[List[str]] = None,
            states: Optional[List[str]] = None,
            passes_tests: Optional[bool] = None,
            not_updated_since: Optional[str] = None,
            has_voted: Optional[str] = None,
            my_comments: Optional[bool] = None
            ) -> dict:
        """
        Get list of available reviews.

        * after: ``int`` (optional)
          A review ID to seek to. Reviews up to and including the specified ``id``
          are excluded from the results and do not count towards ``limit``. Useful
          for pagination. Commonly set to the ``lastSeen`` property from a previous
          query.

        * limit: ``int`` (optional)
          Maximum number of reviews to return. This does not guarantee that ``limit``
          reviews are returned. It does guarantee that the number of reviews
          returned won’t exceed ``limit``. Server-side filtering may exclude some
          reviews for permissions reasons. Default: 1000

        * fields: ``List[str]`` (optional)
          Fields to show, Omitting this parameter or passing an empty value
          shows all fields.

        * author: ``List[str]`` (optional)
          One or more authors to limit reviews by.
          Reviews with any of the specified authors are returned. (**API v1.2+**)

        * changes: ``List[str]`` (optional)
          One or more change IDs to limit reviews by.
          Reviews associated with any of the specified changes are returned.

        * has_reviewers: ``bool`` (optional)
          Limit reviews list to those with or without reviewers.

        * ids: ``List[int]`` (optional)
          One or more review IDs to fetch. Only the specified reviews are returned.
          This filter cannot be combined with the ``limit`` parameter.

        * keywords: ``str`` (optional)
          Keywords to limit reviews by. Only reviews where the description,
          participants list or project list contain the specified keywords are returned.

        * participants: ``List[str]`` (optional)
          One or more participants to limit reviews by.
          Reviews with any of the specified participants are returned.

        * projects: ``List[str]`` (optional)
          One or more projects to limit reviews by. Reviews affecting any of the
          specified projects are returned.

        * states: ``List[str]`` (optional)
          One or more states to limit reviews by. Reviews in any of the specified
          states are returned.

        * passes_tests: ``bool`` (optional)
          Option to limit reviews by tests passing or failing.

        * not_updated_since: ``str`` (optional)
          Option to fetch unchanged reviews. Requires the date to be in the format
          YYYY-mm-dd, for example 2017-01-01. Reviews to be returned are determined
          by looking at the last updated date of the review.

        * has_voted: ``str`` (optional)
          Should have the value ``up`` or ``down`` to filter reviews that have been
          voted up or down by the current authenticated user.

        * my_comments: ``bool`` (optional)
          Filtering reviews that include comments by the current authenticated user.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[int, str, bool, List[str], List[int]]]

        if after:
            params['after'] = after
        if limit:
            params['max'] = limit
        if fields:
            params['fields'] = ','.join(fields)
        if authors:
            params['author'] = authors
            if self.swarm.api_version < 2:
                raise SwarmCompatibleError(
                    'author field is supported from API version >= 2'
                )
        if changes:
            params['change'] = changes
        if has_reviewers is not None:
            params['hasReviewers'] = str(int(has_reviewers))
        if ids:
            params['ids'] = ids
        if keywords:
            params['keywords'] = keywords
        if participants:
            params['participants'] = participants
        if projects:
            params['project'] = projects
        if states:
            params['state'] = states
        if passes_tests is not None:
            params['passesTests'] = str(int(passes_tests))
        if not_updated_since:
            params['notUpdatedSince'] = not_updated_since
        if has_voted:
            params['hasVoted'] = has_voted
        if my_comments is not None:
            params['myComments'] = str(int(my_comments))

        return self.swarm._request('GET', 'reviews', params=params)

    def get_info(self,
                 review_id: int,
                 *,
                 fields: Optional[List[str]] = None
                 ) -> dict:
        """
        Retrieve information about a review.

        * review_id: ``int`` (optional)
          Review id getting information from.

        * fields: ``List[str]`` (optional)
          List of fields to show. Omitting this parameter or passing an empty
          value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'reviews/{}'.format(review_id),
            params=params
        )

        return response

    def get_transitions(self,
                        review_id: int,
                        *,
                        up_voters: Optional[str] = None
                        ) -> dict:
        """
        Get transitions for a review (**v9+**)

        * review_id: ``int``
          Review id getting information from.

        * up_voters: ``str`` (optional)
          A list of users whose vote up will be assumed when determining the
          transitions. For example if a user has not yet voted but would be the
          last required vote and asked for possible transitions we would want to
          include 'approve'

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        if self.swarm.api_version < 9:
            raise SwarmCompatibleError('get_transitions is supported with API v9+')

        params = dict()

        if up_voters:
            params['upVoters'] = up_voters

        response = self.swarm._request(
            'GET',
            'reviews/{}/transitions'.format(review_id),
            params=params
        )

        return response

    def create(self,
               change: int,
               *,
               description: Optional[str] = None,
               reviewers: Optional[List[str]] = None,
               required_reviewers: Optional[List[str]] = None,
               reviewer_groups: Optional[List[str]] = None
               ) -> dict:
        """
        Create a review.

        * fields: ``int``
          Change ID to create a review from.

        * description: ``str`` (optional)
          Description for the new review (defaults to change description).

        * reviewers: ``List[str]`` (optional)
          A list of reviewers for the new review.

        * required_reviewers: ``List[str]`` (optional)
          A list of required reviewers for the new review (**v1.1+**)

        * reviewer_groups: ``List[str]`` (optional)
          A list of required reviewers for the new review (**v7+**)

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict(change=change)  # type: Dict[str, Union[int, str, List[str]]]

        if description:
            data['description'] = description

        if reviewers:
            data['reviewers'] = reviewers

        if required_reviewers:
            data['requiredReviewers'] = required_reviewers
            if self.swarm.api_version == 1:
                raise SwarmCompatibleError(
                    'required_reviewers field is supported from API version > 1'
                )

        if reviewer_groups:
            data['reviewerGroups'] = reviewer_groups
            if self.swarm.api_version < 7:
                raise SwarmCompatibleError(
                    'reviewer_groups field is supported from API version > 6'
                )

        return self.swarm._request('POST', 'reviews', data=data)

    def archive(self,
                *,
                not_updated_since: str,
                description: str) -> dict:
        """
        Archiving the inactive reviews (**v6+**).

        * not_updated_since: ``str``
          Updated since date. Requires the date to be in the format YYYY-mm-dd
          Example ``2017-01-01``

        * description: ``str``
          A description that is posted as a comment for archiving.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        if self.swarm.api_version < 6:
            raise SwarmCompatibleError('archive is supported with API v6+')

        data = dict(
            notUpdatedSince=not_updated_since,
            description=description
        )

        return self.swarm._request('POST', 'reviews/archive', data=data)

    def cleanup(self,
                review_id: int,
                *,
                reopen: Optional[bool] = None
                ) -> dict:
        """
        Clean up a review for the given id (**v6+**).

        * review_id: ``int``
          Review id getting information from.

        * reopen: ``bool`` (optional)
          Expected to be a boolean (defaulting to false). If true then an attempt
          will be made to reopen files into a default changelist

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        if self.swarm.api_version < 6:
            raise SwarmCompatibleError('cleanup is supported with API v6+')

        data = dict()

        if reopen:
            data['reopen'] = reopen

        response = self.swarm._request(
            'POST',
            'reviews/{}/cleanup'.format(review_id),
            data=data
        )

        return response
