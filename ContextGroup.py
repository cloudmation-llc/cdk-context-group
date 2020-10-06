"""
Tools for working with context variable hierarchies in CDK projects.

Classes:

    ContextGroup
"""

class ContextGroup:

    """
    The ContextGroup object represents one or more CDK context variables grouped by a common name.
    """
    def __init__(self, construct) -> None:    
        """
        Creates a new ContextGroup object using access to the context from the provided CDK
        construct node.

        Parameters
        ----------
            construct: aws_cdk.core.ConstructNode
                The CDK node to use for querying context values
        """

        # Get the context groups node from CDK context
        context_groups = construct.node.try_get_context('contextGroups')

        # Look for a context name group manually specified
        self.context_group_name = construct.node.try_get_context('ctxgroup')
        if self.context_group_name is None:
            # Look for a default context group for fallback
            self.context_group_name = context_groups.get('default')

            # Validate
            if self.context_group_name is None:
                raise LookupError('Could not find a context group to load')

        # Get the context group
        context_group = context_groups.get(self.context_group_name)
        
        # Copy context keys to this object
        for key, value in context_group.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        """Generate a string representation of this ContextGroup"""
        
        # Comprehension trickery to print out group attributes as a string (e.g. for print(), logging)
        return 'ContextGroup(' + ', '.join([f'{key}={value}' for key, value in self.__dict__.items()]) + ')'

    def __str__(self) -> str:
        return self.__repr__()