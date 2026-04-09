from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Goal, GoalStatus
from .selectors import get_active_goals
from .services import create_goal, update_goal


class GoalServiceTests(TestCase):
    def test_create_goal_generates_slug(self):
        goal = create_goal(
            title="Ship MVP",
            description="First pass",
            type="career",
            status="active",
            priority="high",
        )

        self.assertEqual(goal.slug, "ship-mvp")

    def test_update_goal_sets_completed_at_for_completed_status(self):
        goal = create_goal(
            title="Finish docs",
            description="",
            type="learning",
            status="active",
            priority="medium",
        )

        updated = update_goal(
            goal=goal,
            title="Finish docs",
            description="",
            type="learning",
            status=GoalStatus.COMPLETED,
            priority="medium",
            deadline=None,
            is_archived=False,
        )

        self.assertIsNotNone(updated.completed_at)

    def test_update_goal_clears_completed_at_when_status_reopens(self):
        goal = create_goal(
            title="Finish docs",
            description="",
            type="learning",
            status=GoalStatus.COMPLETED,
            priority="medium",
        )

        updated = update_goal(
            goal=goal,
            title="Finish docs",
            description="",
            type="learning",
            status=GoalStatus.ACTIVE,
            priority="medium",
            deadline=None,
            is_archived=False,
        )

        self.assertIsNone(updated.completed_at)

    def test_update_goal_can_archive_goal(self):
        goal = create_goal(
            title="Archive me",
            description="",
            type="personal",
            status="active",
            priority="low",
        )

        updated = update_goal(
            goal=goal,
            title="Archive me",
            description="",
            type="personal",
            status="active",
            priority="low",
            deadline=date(2026, 4, 9),
            is_archived=True,
        )

        self.assertTrue(updated.is_archived)


class GoalModelTests(TestCase):
    def test_slug_is_immutable(self):
        goal = create_goal(
            title="Immutable slug",
            description="",
            type="career",
            status="active",
            priority="high",
        )

        goal.slug = "changed-slug"
        with self.assertRaises(ValidationError):
            goal.full_clean()


class GoalSelectorTests(TestCase):
    def test_get_active_goals_returns_only_non_archived_active_goals(self):
        active_goal = create_goal(
            title="Visible goal",
            description="",
            type="career",
            status="active",
            priority="high",
        )
        create_goal(
            title="Paused goal",
            description="",
            type="career",
            status="paused",
            priority="medium",
        )
        create_goal(
            title="Archived goal",
            description="",
            type="career",
            status="active",
            priority="medium",
            is_archived=True,
        )

        self.assertEqual(list(get_active_goals()), [active_goal])
