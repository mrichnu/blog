---
title: "Multi-Cloud Is The Default In Higher Ed"
tags: cloud
---

If your enterprise is starting today, you should absolutely follow the advice of
[Corey Quinn](https://www.lastweekinaws.com/blog/A_MultiCloud_Rant/) and
standardize on a single cloud provider. In the world of higher education,
however, the enterprise began hundreds of years ago and things look a little
different.

<!-- more -->

I have worked in small and large private enterprises before joining Northwestern
University in 2007. I'm aware that Northwestern, a highly selective private
research institution, differs in significant ways from other colleges and
universities. But I've learned enough here to respectfully disagree about the
need for a multi-cloud presence when it comes to higher education in general.

## Higher Ed Is Distinct

The institution I work for was founded 171 years ago. Harvard University, which
charted the course for American higher education and whose example every school
is aware of and in some way responding to, traces its founding back nearly 400
years to 1636. Obviously - obviously! - these institions have grown and changed
enormously in that time, and we don't sit around talking about how [John
Evans](https://en.wikipedia.org/wiki/John_Evans_(Colorado_governor)) and
[Frances Willard](https://en.wikipedia.org/wiki/Frances_Willard) would have
addressed today's IT challenges. But there is an unbroken line of decisions and
institutional contexts that have led us, and other schools, to where we are
today. 

A non-exhaustive list of the ways higher ed differs from the corporate (and even
other non-profit)worlds:

- **Primacy of consensus:** It's said of faculty that a vote of 99-1 is
  considered a tie. The committee-led decisionmaking process extends beyond the
  faculty senate and into the IT organization.
- **Diffuse decisionmaking responsibility:** In theory the division of
  responsibility between the board of trustees, the president, the provost, the
  VP for research, individual deans (and associate deans), the CIO, the
  executive vice president, etc. can be clearly defined and articulated. In
  practice these divisions and reporting lines are very hazy and
  relationship-based. 
- **Institutional mission:** You wouldn't necessarily know it from our
  fundraising campaigns, but the mission of a university is to create and
  disseminate knowledge, not to make money.
- **Researcher incentives:** This was the maybe the most surprising thing for me
  personally when I started here. Individual researchers operate more like small
  businesses, bringing in grant money to support their own work. They have
  mostly free rein to staff their labs and research teams as they see fit, and
  pay rent to the university in the form of "indirect costs" (a portion of the
  grant award money which the university keeps, the percentage varies by school)
  for the use of its facilities. The researchers are incentivized to bring in as
  much grant money as possible, and the requirements of different grants and
  research projects may push them towards multiple IT solutions.
- **Cross-institutional collaboration:** Not only will faculty members
  collaborate closely with their peers at other institutions, but staff will as
  well. I spend far more time directly sharing knowledge and collaborating with
  my peers at other, "rival" schools than would ever be possible in private
  enterprise.
- **Alumni networks:** A real thing. And occasionally highly placed in a
  vendor's sales team.
- **Students:** Not only a source of brilliant new ideas and energy, but also a
  large source of very cheap, highly motivated, and occasionally shockingly
  skilled labor that turns over very quickly. (See: Alumni networks)

## Multi cloud is the default

The above factors drive the vast majority of American higher education
institutions to have a presence in each of the major cloud providers. For
example:

The IT director of a small college within the university listens to her
developers and chooses Amazon Web Services as their platform of choice to build
new applications. She makes her case to the dean, who gives the thumbs up. The
college is spending its own funds to run these cloud environments, and there is
no policy that specifically prohibits using AWS, so away they go.

The medical school leadership decides to build a data warehouse to store
clinical data from the university's affiliated hospital so that researchers can
access it safely for their projects. A new core facility (another form of small
business within a university -- they own equipment or resources needed by
multiple faculty members and charge for its use) is created and its director
hires a consulting partner to build it. The consulting partner makes a
convincing case that Microsoft Azure is the right cloud to build this, and there
is no policy that specifically prohibits using Azure. So away they go.

An enterprising PhD student in a molecular biology lab builds a data portal
using Google Cloud to share fungus genome data, because there is no policy that
specifically prohibits using Google Cloud and even if there were he'd have
ignored it. The data portal quickly becomes a widely used and relied-upon
resource across the entire field of fungal genomics. The student graduates but
the data portal must be kept running to support the ongoing work in the field.
Congratulations, the IT department now owns a fungal genomics data portal.

These are only slightly altered scenarios from my real experience and the same
happens at research institutions across the country. 

A valid criticism of the above scenarios is: why wasn't the central IT cloud
team in the loop to guide these decisions? And absolutely they should be, but it
does require enormous time and effort to build the relationships and trust that
would get the decisionmakers to include the cloud team. Because for the reasons
stated above, and because of the self-service nature of cloud services in
general, *they are fully empowered to do it themselves*.

Multi-cloud is simply a fact of life at institutions like this, and those of us
in cloud governance must put in the work to make the workloads in each cloud
environment as safe, secure, and cost-effective as possible.

## Single cloud can happen

All that said, there *are* instances of similar universities that have decided
to go all-in on a single cloud provider. That is only possible when there is a
CIO with a clear vision, an iron will, and a time machine.

The schools that have done this made the decision very early on (think 2012-ish)
in their cloud journey. I don't want to say that moving a large research
university in 2023 from a multi-cloud presence to a single cloud provider is
impossible, but I would certainly want to have a very detailed conversation with
anyone who was thinking of attempting this. 

I would also argue that schools without a large research presence, meaning small
liberal arts colleges, teaching and learning-focused public universities, etc.
should, if they are thinking of using public cloud services at all, focus on a
single provider for all of the reasons laid out by [Corey
Quinn](https://www.lastweekinaws.com/blog/A_MultiCloud_Rant/), [Lydia
Leong](https://cloudpundit.com/2021/10/14/multicloud-failover-is-almost-always-a-terrible-idea/)
etc.

## Takeaways

A few parting thoughts:

If you work in higher ed IT and are wondering whether to try to push your
institution to use a single cloud, I think it depends on where in the
organization you sit. If you are in distributed/departmental IT, then yes I
think it makes sense to lighten the cognitive and operational load and focus on
a single cloud provider for your team or department.

If however you're in central IT and need to keep things running smoothly for
your colleagues and customers in the distributed schools and departments, you
have no choice but to make the best of multicloud.

That means, at a minimum:

- Simple, clearly-defined standards that you communicate *constantly*
- Hard preventive guardrails to prevent dangerous (and/or expensive) operations
- Regular checkins with cloud account owners
- Wear sunscreen and get plenty of rest!
