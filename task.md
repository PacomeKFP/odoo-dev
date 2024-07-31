## Exercise

Add a stat button to property type.

- Add the field `property_type_id` to `estate.property.offer`. We can define it as a related field on `property_id.property_type_id` and set it as stored.

Thanks to this field, an offer will be linked to a property type when it’s created. You can add the field to the list view of offers to make sure it works.

- Add the field `offer_ids` to `estate.property.type` which is the One2many inverse of the field defined in the previous step.
- Add the field `offer_count` to `estate.property.type`. It is a computed field that counts the number of offers for a given property type (use `offer_ids` to do so).

At this point, you have all the information necessary to know how many offers are linked to a property type. When in doubt, add `offer_ids` and `offer_count` directly to the view. The next step is to display the list when clicking on the stat button.

- Create a stat button on `estate.property.type` pointing to the `estate.property.offer` action. This means you should use the `type="action"` attribute (go back to the end of Chapter 9: Ready For Some Action? if you need a refresher).

At this point, clicking on the stat button should display all offers. We still need to filter out the offers.

- On the `estate.property.offer` action, add a domain that defines `property_type_id` as equal to the `active_id` (= the current record, [here is an example](#)).
