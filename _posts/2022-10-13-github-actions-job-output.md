---
title: "Using GitHub Actions Job Outputs and Environment Files"
tags: coding
---

I've been fighting my GitHub Actions workflow all day and finally won, so I
might as well get a quick blog post out of it!

<!-- more -->

GitHub's [Actions](https://docs.github.com/en/actions) CI/CD service is pretty
flexible and great. And GitHub's documentation is stellar overall, but there is
a very useful yet under-documented feature called "Job outputs". Namely, your
workflow Jobs (remember, a Job is a collection of Steps) can have outputs that
can be used by other jobs. This is distinct from the "environment files" feature
which allows *Steps* within a single *Job* to share variables.

## Rules of thumb:
1. To share information between *Steps* within a single *Job*, use [environment
   files](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#environment-files).
2. To share information between separate *Jobs*, use [Job
   outputs](https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs).

## Using environment files

The GitHub documentation's example here is straightforward and should work for
most use cases:

```yaml
{% raw %}
steps:
  - name: Set the value
    id: step_one
    run: |
      echo "action_state=yellow" >> $GITHUB_ENV
  - name: Use the value
    id: step_two
    run: |
      echo "${{ env.action_state }}" # This will output 'yellow'
{% endraw %}
```

Essentially, you append a key=value pair to the special `$GITHUB_ENV` file, and
that key is an environment variable in subsequent steps of the same job. Easy
enough.

## Using Job outputs

Here, and this may be due to the recent deprecation of the `::set-output`
command so the docs haven't caught up yet, the documentation leaves some very
important steps out. Below is a simple template you can use:

```yaml
{% raw %}
jobs:
  job1:
    outputs:
      myoutput: ${{ steps.step1.outputs.myoutput }}
    
    steps:
    - name: set output
      id: step1
      run: |
        echo "myoutput='hello world'" >> $GITHUB_OUTPUT

  job2:
    needs: job1

    steps:
    - name: retrieve output
      run: |
        echo ${{ needs.job1.outputs.myoutput }}
{% endraw %}
```

Job 2 here will print "hello world". The important things to note are:
- The Step that outputs something must have an `id`, and append its output to
  the special `$GITHUB_OUTPUT` file as a key=value pair
- The Job containing the step (here, `job1`) must have an `outputs:` block where
  it sets the value of the output by retrieving the step's output. The Job
  output name doesn't necessarily have to be the same as the Step output name
  although I don't know why you'd want them to be different.
- The Job that wants to consume the output (here, `job2`) must have a `needs:`
  block where it declares which job's output it will need.
- The Step that wants to use the output can access it via the `{% raw %}${{ needs.<job
  id>.outputs.<output name> }}{% endraw %}` variable.

## Tips

1. It's much simpler conceptually to have fewer jobs with more steps. Only use
   multiple jobs when you need e.g. to apply changes to multiple environments or
   run steps conditionally.

2. You can enable [debug
   logging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging)
   for your workflow if it's not behaving as expected.

3. Wear sunscreen and get plenty of rest!