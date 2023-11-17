import boto3

def setup_cloudwatch_event(lambda_function_arn):
    cloudwatch_events_client = boto3.client('events')

    # CloudWatch event rule name
    rule_name = 'PyCloudDeployerDailyTrigger'

    # Schedule expression for CloudWatch event
    schedule_expression = 'cron(0 6 * * ? *)'

    # Create or update the rule
    cloudwatch_events_client.put_rule(
        Name=rule_name,
        ScheduleExpression=schedule_expression,
        State='ENABLED'
    )

    # Link the rule to the Lambda function using ARN
    cloudwatch_events_client.put_targets(
        Rule=rule_name,
        Targets=[{'Id': '1', 'Arn': lambda_function_arn}]
    )

    print(f"CloudWatch Event Rule '{rule_name}' set to trigger Lambda function daily.")