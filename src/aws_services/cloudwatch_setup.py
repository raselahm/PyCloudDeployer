import boto3

def setup_cloudwatch_event(lambda_function_name):
    cloudwatch_events_client = boto3.client('events')
    lambda_client = boto3.client('lambda')

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

    # Link the rule to the Lambda function
    cloudwatch_events_client.put_targets(
        Rule=rule_name,
        Targets=[{'Id': '1', 'Arn': lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']}]
    )

    print(f"CloudWatch Event Rule '{rule_name}' set to trigger Lambda function '{lambda_function_name}' daily.")