[![codecov](https://codecov.io/gh/notyumin/SimpCity/branch/development/graph/badge.svg?token=DBJ0D3XJNB)](https://codecov.io/gh/notyumin/SimpCity)
# SimpCity Software Development Journal

## Table of Contents

- [SimpCity Software Development Journal](#simpcity-software-development-journal)
  - [Table of Contents](#table-of-contents)
  - [Choosing Our SDLC](#choosing-our-sdlc)
    - [1. Waterfall](#1-waterfall)
    - [2. V-Shaped](#2-v-shaped)
    - [3. Iterative](#3-iterative)
    - [4. Evolutionary](#4-evolutionary)
    - [5. Agile](#5-agile)
    - [Weightage](#weightage)
    - [Decision Matrix](#decision-matrix)
    - [Verdict](#verdict)
  - [Language Chosen](#language-chosen)
  - [Our Workflow](#our-workflow)

## Choosing Our SDLC

To start off our project, we first had to choose an SDLC. To do that, we analysed 5 SDLCs in detail before finally using a Decision Matrix to evaluate them.

Criteria used for analysis:

1. **Preparation Required**: Work needed before development can begin `(less prep = higher score)`
2. **Flexibility**: Allowance for changes in requirements `(more allowance = higher score)`
3. **Speed**: Total time needed to get working software `(less time = higher score)`
4. **Customer Interaction**: To what extent customer is able to interact with the product during development `(more interaction = higher score)`
5. **Software Resillience**: How likely the software is to have unexpected issues and bugs `(fewer issues = higher score)`
6. **Fulfills Requirements**: How close the end product will be to the initial requirements `(closer = higher score)`

### 1. Waterfall

>The Waterfall SDLC is a very traditional style of software development which follows a strict linear path from phase to phase. It is possible to return to earlier phases, but it is not recommended because it is very expensive (in terms of time, money and manpower) to do so.
>
>However, its rigidity is also its strength, because the software produced will follow exactly or at least very closely to the requirements provided by the customer, and will likely be very stable. This SDLC is recommended if all the requirements of the project are known upfront, and are not subject to change over the course of the project.

<details><summary> Preparation Required: 4/10 </summary>

`Requires all requirements to be understood upfront in the analysis phases.`
</details>

<details><summary>Flexibility: 1/10</summary>

`Waterfall is extremely rigid. Adding requirements, skipping phases or returning to past phases are not recommended.`
</details>

<details><summary>Speed: 3/10</summary>

`There is a heavy emphasis on documentation and testing from phase to phase, so it is not a fast SDLC.`
</details>

<details><summary>Customer Interaction: 1/10</summary>  

`Product can only be seen and tested by the customer in the late stages of the Waterfall process`
</details>

<details><summary>Software Resilience: 10/10</summary>

`The strong emphasis on documentation and testing from phase to phase results in extremely resilient software.`
</details>

<details><summary>Fulfills Requirements: 10/10</summary>

`Waterfall methodology development sticks extremely closely to the original requirements given, and requirements are never (or very rarely) changed. Thus, Water Methodology usually produces software in line with the original specification.`
</details>

### 2. V-Shaped

>The V-shaped SDLC is similar to waterfall in the sense that it has sequential, clearly differentiated stages of development.
>
>Adaptability is not a strong suit of the SDLC because of this. At the start of the project, the requirements must be fully known as various tests are designed for the project at the start. Changing requirements mid-cycle would result in much wasted time.
>
>The SDLC places a strong emphasis on testing, as throughout development several types of tests are designed in the first half and then validated in the second half.
>
>The client is present in the process at the initial requirement analysis stage and the final acceptance testing stage.
>
>As such this SDLC should be used if reliability of the product is extremely important, the client is not interested in being fully involved in the process, and the requirements of the project are not likely to change.

<details><summary>Ease of planning: 4/10</summary>  

`Testing phases are planned throughout the left side of the "V"`
</details>

<details><summary>Flexibility: 1/10</summary>

`Strict stages of development and extensive planning means that once development starts it is difficult and costly to add new features`
</details>

<details><summary>Speed: 5/10</summary>  

`Neither fast nor slow - adheres to a stipulated timeline`
</details>

<details><summary>Customer Interaction: 5/10</summary>  

`Customer will voice their requirements at the start of the project and be present for acceptance testing.`
</details>

<details><summary>Software Resilience: 10/10</summary>  

`Strong emphasis on verification & validation of product.`
</details>

<details><summary>Fulfills Requirements: 10/10</summary>  

`This model expects that the requirements are set out thoroughly at the start and then developed for later. Thus, the end product will meet the initial requirements faithfully.`
</details>

### 3. Iterative

>The iterative process is the practice of building, refining, and improving a project, product, or initiative. Teams that use the iterative development process create, test, and revise until they’re satisfied with the end result. You can think of an iterative process as a trial-and-error methodology that brings your project closer to its end goal. 
>
>Iterative processes are a fundamental part of lean methodologies and Agile project management—but these processes can be implemented by any team, not just Agile ones. During the iterative process, you will continually improve your design, product, or project until you and your team are satisfied with the final project deliverable.

<details><summary>Ease of planning: 5/10</summary>  

`As you learn new things during the implementation and testing phases, you can tweak your iteration to best hit your goals—even if that means doing something you didn’t expect to be doing at the start of the iterative process.` 
</details>

<details><summary>Flexibility: 5/10</summary>  

`The first step of the iterative process is to define your project requirements. Changing these requirements during the iterative process can break the flow of your work, and cause you to create iterations that don’t serve your project’s purpose.`
</details>

<details><summary>Speed: 7/10</summary>  

`Because the iterative process embraces trial and error, it can often help you achieve your desired result faster than a non-iterative process.`
</details>

<details><summary>Customer Interaction: 8/10</summary>  

`The software is produced in the early stages of the life cycle, and thus the customer is able to evaluate and provide feedback for the product early on. The customer can also provide feedback for each iteration as each iteration produces working software. However, there is not as much room for change as in Agile or Evolutionary.`
</details>

<details><summary>Software Resilience: 8/10</summary>  

`The software is tested during each iteration, which means issues can be identified at their early stages when they are still relatively easy to fix. `
</details>

<details><summary>Fulfills Requirements: 7/10</summary>  

`Changing requirements is less costly than Waterfall/V-shaped, but still incurs quite a cost and hence is not recommended.` 
</details>

### 4. Evolutionary

>Evolutionary SDLC is a combination of Iterative and Incremental model of the software development life cycle. When implementing this model, initial requirements and architecture envisioning should be done. This means based on a vague notion of the client’s requirements, core modules/skeleton of the system is being developed. After each increment, based on the review given by the clients, further iterations are performed, often changing the requirements over time. 
>
>This SDLC is recommended for research and development projects. Alternatively, this model can be implemented when a project has requirements that are not clear or will be evolve during the development cycle.  

<details><summary>Preparation Required: 7/10</summary>  

`Not much initial planning is done as requirements are not well-defined and is susceptible to change with client feedback.` 
</details>

<details><summary>Flexibility: 8/10</summary>  

`Accommodates unexpected and changing requirements, able to implement missing functionalities. With constant feedback, positive revisions can be done in the next increment.`
</details>

<details><summary>Speed: 8/10</summary>  

`Since minimal viable product is delivered, development time is reduced, making product delivery relatively fast. However, in the long run, timeline of project may extend (within client's expense) if client has many requirements to change or add.`
</details>

<details><summary>Customer interaction: 10/10</summary>  

`Clients are able to test the product at the end of each increment, accurately elicit user requirements during the delivery of product.`
</details>

<details><summary>Software resilience: 9/10</summary>  

`With the strong facilitation of client’s feedback and constant thorough testing, chances of errors in the core modules are significantly reduced. However, with minimal viable product being delivered in each increment, potential small bugs may arise.`
</details>

<details><summary>Fulfills Requirements: 1/10</summary>  

`The model expects the project and its features to evolve over time. However, due to the known requirements of the project and a concrete view of the end-product, it is highly unlikely this model is able to effectively fulfill the project's requirements.`
</details>

### 5. Agile

>The agile SDLC methodology is based on a cyclical, iterative development process with focus on process adaptability and customer satisfaction via rapid delivery of working software.
>Work is done in regularly iterated cycles known as sprints, with each sprint typically lasting 2 to 4 weeks.
>At the start of the project, core requirements are known but will be expected to change over time as the project progresses.
>
>This SDLC places a strong emphasis on producing working software based on the requirements provided as quickly as possible, with test-driven development aimed to implement features incrementally.
>It is highly adaptable to changing requirements as each sprint will attempt to implement a set number of features, which are decided at the end of the previous sprint.
>While documentation may be brief, the features and changes implemented in each sprint must be clearly documented to display work done to the client.
>
>The client is present throughout the process to validate the work done and will likely provide additional requirements throughout the entire SDLC.
>As such, this SDLC should be used if there is a need to deliver working software as soon as possible, with requirements that are highly likely to change.

<details><summary>Planning required: 8/10</summary>  

`Requirements are not well-defined and is susceptible to change with client feedback.`
</details>

<details><summary>Flexibility: 8/10</summary>  

`This SDLC is highly adaptable to change, with constant delivery of working software and client feedback with each sprint.`
</details>

<details><summary>Speed: 8/10</summary>


`With a focus on delivering working software by the end of each sprint, product delivery is quick and client is able to give feedback.`

`While overall production time may be longer than other SDLC models due to changing requirements, it is able to deliver working software quickly.`


</details>

<details><summary>Customer Iteration: 10/10</summary>  

`The customer is able to view documentation, albeit brief documentation, and test the software produced in each sprint. This SDLC allows for constantly changing requirements as features are implemented in sprints of 2 to 4 weeks.`
</details>

<details><summary>Software resilience: 5/10</summary>  

`With a focus on delivering constant working software in short sprints, unforseen bugs are likely to arise due to new features being implemented. However, as features are being developed and implemented individually, it is easier to debug the software.`
</details>

<details><summary>Fulfills requirements: 5/10</summary>  

`While a large amount of requirements are known, they are also expected to change. Thus, agile might fit the project.`
</details>

### Weightage

>To make sure that our decision matrix could correctly reflect the importance of each criteria in the context of our project, we assigned a weightage to each criteria.

<details><summary>Preparation Required: 0.15</summary>

`We wanted to do minimal planning so that we could start our project as soon as possible. However, the weightage was dropped slightly since the requirements are already generated for us so less planning is required in the first place.`
</details>

<details><summary>Flexibility: 0.25</summary>

`The client made it clear up front that there might be changes to the features in the future, and thus flexibility of requirements is very important.`
</details>

<details><summary>Speed: 0.25</summary>  

`The project has a rather tight schedule and as such speed to get the product out is very important.`
</details>

<details><summary>Customer Interaction: 0.1</summary>  

`The client did not request for very frequent updates, thus we did not place a high weightage on customer interaction. However, we did not completely exclude it from consideration as well because chances are the client would want to see the progress at times.`
</details>

<details><summary>Software Resilience: 0.15</summary>  

`The software requirements are quite small-scale, and thus software resilience is not as important as it might be in a large-scale project. However, it does not have a very low score either because the client has low tolerance for buggy software.`
</details>

<details><summary>Fulfills Requirements: 0.3</summary> 

`We were provided a full set of requirements by the client, and thus it is very important that the each requirement is fulfilled.`
</details>

### Decision Matrix

| | Preparation Required (Weight: 0.15) | Flexibility (Weight: 0.25) | Speed (Weight: 0.25) | Customer interaction (Weight: 0.1) | Software Resilience (Weight: 0.15) | Fulfills Requirements (Weight: 0.3) | Final Score |
| ------------ | -- | -- | -- | -- | -- | -- | ---- |
| Waterfall    | 4  | 1  | 3  | 1  | 10 | 10 | 6.2  |
| V-shaped     | 2  | 1  | 5  | 5  | 10 | 10 | 6.8  |
| Evolutionary | 7  | 8  | 8  | 10 | 9  | 1  | 7.7  |
| Iterative    | 5  | 5  | 7  | 8  | 8  | 7  | 7.85 |
| Agile        | 8  | 8  | 8  | 10 | 5  | 5  | 8.45 |

### Verdict

In the end, our chosen SDLC was **Agile** because it fit our requirements the best. It offers high flexibility, speed and customer interaction, while not deviating too much from original requirements. 

## Language Chosen

todo

## Our Workflow

todo
